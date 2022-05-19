from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import CategorySerializer
from .models import Category, User
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from dotenv import load_dotenv
import os, requests, json
from .utils import *

load_dotenv()

# load environment variables
RAINFOREST_API = os.environ.get("RAINFOREST_API")
KWEAPI = os.environ.get("KWEAPI")


def index(request):
    """Returns homepage and handles category search function"""
    if request.method == "POST":
        query = request.POST["q"]
        if query == "":
            messages.error(
                request,
                "Invalid search query. Please try again.",
            )
        else:
            return redirect("search_results", q=query)

    return render(request, "amazon_niche_finder/index.html")


def search_results(request, q):
    """Returns category search results"""

    # take search query and retrieve all results.
    search = Category.objects.filter(
        cat_link__icontains=q).order_by("cat_link") | Category.objects.filter(
            cat_name__icontains=q).order_by("cat_name")

    # Handle if there are no results found
    if len(search) == 0:
        no_results = "There were no search results found. Try a broader search term."
        results = ""
    else:
        no_results = ""
        results = search

    return render(
        request,
        "amazon_niche_finder/search-results.html",
        {
            "no_results": no_results,
            "results": results,
            "search_query": q.title(),
        },
    )


def show_categories(request):
    """Returns full tree listing of all categories in database"""
    categories = Category.objects.all()

    return render(
        request,
        "amazon_niche_finder/all-categories.html",
        {"categories": categories},
    )


def show_subcats(request, id):
    """Returns a detail page containing bestsellers for a chosen category
    and the ability to keyword search golden ratio data."""

    # Get requested Category and all descendants.
    # Some category names are duplicated in the db due to design of the CSV.
    # (eg. Die-Cast Vehicles).Filter the Category search to get first result that
    # also has a bestseller link
    obj = Category.objects.filter(pk=id,
                                  cat_bestsellers_link__isnull=False).first()

    # Credit: https://stackoverflow.com/questions/50596036/how-to-show-a-certain-number-of-levels-in-django-mptt
    get_subs = obj.get_descendants().filter(level__lte=obj.level + 9)

    # set up the request parameters
    params = {
        "api_key": RAINFOREST_API,
        "type": "bestsellers",
        "url": obj.cat_bestsellers_link,
    }

    # make the http GET request to Rainforest API
    api_result = requests.get("https://api.rainforestapi.com/request", params)

    # JSON response from Rainforest API
    res = api_result.json()

    # Paginate results
    paginator = Paginator(res["bestsellers"], 9)  # Show 9 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "amazon_niche_finder/cat-details.html",
        {
            "category": obj,
            "subs": get_subs,
            "page_obj": page_obj,
        },
    )


def check_keyword(request):
    """Return Golden Ratio results"""

    # Handle if not POST request
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    response = json.loads(request.body)

    # Handle if empty input submitted
    if response.get("keyword") == "":
        return JsonResponse({"error": "Keyword Field Cannot Be Blank."},
                            status=400)
    else:

        # Get form submission input
        data = response.get("keyword")

        # Keywords Everywhere API
        my_data = {
            "dataSource": "gkp",
            "kw[]": [data],
        }

        my_headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {KWEAPI}",
        }
        response = requests.post(
            "https://api.keywordseverywhere.com/v1/get_keyword_data",
            data=my_data,
            headers=my_headers,
        )

        # Handle if request is successful
        if response.status_code == 200:
            res = response.json()
            true_volume = int(res["data"][0]["vol"])
            credit_left = int(res["credits"])
            all_in_title = check_ait(data)
            zero_volume = 0

            # handle divide by 0 -- typically 0 search volume is a good thing
            if true_volume == 0:
                zero_volume = all_in_title * 3
                golden_ratio = (all_in_title) / zero_volume
            else:
                golden_ratio = (all_in_title) / true_volume
        else:
            print("An error occurred\n\n", response.content.decode("utf-8"))

    return JsonResponse(
        {
            "true_volume": true_volume,
            "zero_volume": zero_volume,
            "credits_left": credit_left,
            "all_in_title": all_in_title,
            "golden_ratio": f"{golden_ratio:.2f}",
        },
        status=200,
    )


@api_view(["GET"])
def get_bestseller(request, id):
    """Serializer for retrieving bestseller info. Easier to handle in JS."""
    try:
        cat = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        serializer = CategorySerializer(cat)
        return Response(serializer.data)
