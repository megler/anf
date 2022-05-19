# Amazon Niche Finder (ANF)

## Overview

Amazon Niche Finder (ANF) is an app that allows affiliate marketers (people who earn a commission by promoting a product or service made by another retailer or advertiser) to look through all of amazon's bestseller categories and discover products/niches.  (niche: a specialized segment of the market for a particular kind of product or service.)

ANF further allows a user to do preliminary research to determine if a niche possibility matches [Golden Ratio](https://sirlinksalot.co/keyword-golden-ratio/) criteria. The Golden Ratio, in short, divides Google allintitle search results by normal (not allintitle) search volume, where preferred search volume is 250 or less. The
resulting ratio gives you an idea of how easy a topic would be to rank on page one of Google in a relatively short period of time.

ANF is mainly an idea generator. Many affiliate marketers use Amazon as a low barrier to entry for affiliate marketing. ANF allows the user to look through categories and if they see something that interests them (eg. 'cat hammocks'), they can use the built in keyword search tool to see if the idea is worth pursuing.

## ANF Pages

### Homepage

The homepage has 3 main features:

1. Category Search
2. Quick Links to main parent categories
3. Link to entire category listing (over 27k categories up to 9 levels deep)

#### Category Search

The homepage features a search bar that allows a user to search for possible categories without having to dig through nested menus. This is a somewhat limied feature as the search must at least partially match a category name.

For example, a search of "dog beds" will return nothing as there is no bestseller page for "dog beds." However, the user could search for "dog" or "pet bed" and would find results that could lead to dog beds.

If a user has a keyword in mind, it's worth trying the search, but if no results are found, it is recommended to try a broader search (eg. 'dog' or 'pet' vs 'dog bed') or to look for a parent category in either the quick links or full category results that could possibly hold a relevant category. (eg. Pet Supplies in quick links).

#### Quick Links

At the bottom of the homepage are 18 quick links. These are the main Amazon categories which contain bestseller pages and/or child categories which contain bestseller pages.

#### Entire Category Listing

Under the search bar is a link that will take the user to a page listing all Amazon categories even if they don't have a bestseller page. Categories which do have a bestseller page will be properly linked.

### Detail Page

The details page (all-categories.html) allows a user to see the first page of Amazon's bestselling products for the selected category (eg. 'hammocks'). Django pagination is used to limit results to 10 per page. In the left sidebar, there is a search bar. The search bar allows the user to type or copy/paste in a search term and see if it fits [Golden Ratio](https://sirlinksalot.co/keyword-golden-ratio/) criteria.

JavaScript analyzes the Golden Ratio output and color codes the result. If the ratio is worth exploring, it will be green, a "maybe" will be yellow, and a "too high" will be red. Also, in the event there is 0 search volume for a keyword, instead of returning a "divide by 0" error, the view runs an alternative equation and JavaScript adds a tooltip to the volume div with instructions on why this niche may be worth [further investigation](https://www.singlegrain.com/seo/zero-search-volume-keywords/).

When a Golden Ratio keyword search is performed, the remaining credits for Keywords Everywhere (see API's and Modules below) are displayed. This is just a courtesy so you know when you're getting low on search credits.

When looking at a detail page, the product listing can help generate niche ideas. For example, you wouldn't search "Wise Owl Outfitters Camping Hammock" as that is too specific. But it may be worth looking at "Camping Hammock" or "Portable Camping Hammock" which are all terms one would see in the product names displayed. Again, the main idea of ANF is idea generation.

** Please note ** When looking at some of the products listed for a given category, they may look out of place and very much mis-categorized. This isn't an error of the API. Checking the actual matching Amazon bestseller page will show the same products. This is likely because independent sellers are trying to rank their product as a 'bestseller' and are cheating the system by saying, for example, "baby wipes" should be listed under "fuel injection parts." 

## API's and Modules

### Python-Dotenv

Environment variables are stored in a .env file and handled by [Python-Dotenv](https://pypi.org/project/python-dotenv/).

### Rainforest API

The bestseller products are generated using [Rainforest API](https://www.rainforestapi.com/). This is a premium API ($9.00/mo for 500 requests, then $45.00/mo up to 10k results). Moving forward, I'll either scrape the results myself or find a way to get [Python Amazon Paapi](https://github.com/sergioteula/python-amazon-paapi) - which is free - to generate the desired results. 

### Keywords Everywhere API

[Keywords Everywhere](https://keywordseverywhere.com/) is a premium API ($10.00 flat for 100k results). They provide both a Chrome extension as well as a developer API. While the API provides pretty in-depth results for keywords, ANF uses it for keyword search volume only.

Moving forward, functionality will be added where a user can input their KWE API key to run as many searches as they have credit.

The KWE API is used on the Detail page where a user can do preliminary keyword research around Golden Ratio criteria. The API itself just returns search volume. The Golden Ratio is calculated by Python in the `check_keyword` view.

### Amazon Category CSV

The Category model is populated with over 27k nested Amazon categories provided by (https://amazon-categories-sub-categories-list.blogspot.com/)[https://amazon-categories-sub-categories-list.blogspot.com/]. The more I've worked with it, the more I believe in the future I'll scrape the data myself. After working with the list over the past month, the data is not consistent. There was mixed capitalization, mixed use of "and" and "&," etc.

That said, moving forward, Amazon will be checked twice a year to new categories or changes to existing ones. I don't believe they changed/add categories frequently.

### Modified Pre-Ordered Tree Traversal (mptt)

All pages that show a tree of categories were built using [Modified Pre-Ordered Tree Traversal- mptt](https://django-mptt.readthedocs.io/en/latest/index.html). While this module is no longer supported, it was the most documented on Stack Overflow for troubleshooting. This was, by far, the most time consuming portion of the entire application. 

The mptt module works in two capacities. First, it turns a specified model (categories) into a pre-ordered tree, performing the heavy lifting of interrelating nested levels. Next it gives the developer tags which can be used in a Django template to recursively render everything as a nested tree.

The documentation gives you a very straightforward way to display a recursive nested UL list with a simple copy and paste. The challenge arose when trying to incorporate JavaScript to make the nested UL interactive. The default mptt code was no longer useful. The code for that solution is found in the category-tree.html template component as well as the bestseller-detail-content.html component.

## Django Custom Admin Commands

There is no admin or superuser built for ANF. The models are created for future use, but are not implemented in any meaningful way. Future plans will be to have a user area where logged in users can save Golden Ratio searches to refer back to.

There are 2 custom management commands. Import and Linkadder. [From Docs:](https://simpleisbetterthancomplex.com/tutorial/2018/08/27/how-to-create-custom-django-management-commands.html)
 
### Run import
run `python manage.py import --path ./amazon_niche_finder/imports/amazon_categories.csv`

The import command takes the CSV saved in /imports and coverts it into a mptt model. See above on mptt for further detail on how this function works.

### Add bestseller links after import 
run `python manage.py linkadder`

The CSV comes with a generic Amazon link to a given category. Since the entire purpose of ANF is to look at bestseller categories, a method needed to be written to query Amazon and confirm if a category has a bestseller page and if so, create a link to that page.

Amazon Bestseller links have a common pattern:

`https://amazon.com/gp/bestsellers/{category-name}/{node-id}`

Looking at the CSV links, patterns were observed that could utilize regex. Three regex patterns were created.

1. Regex for id
2. Two different regex for category name based on how the CSV link was structured.

## Credits:

Most things are credited inline, but a few are not.

[Nested dropdown for mptt]
(https://stackoverflow.com/questions/64827786/rendering-mptt-structure-with-open-close-possibility-in-django-template)

### Images:

Homepage Seattle Market Background Image - [Photo by Amanda Grove from Pexels:](https://www.pexels.com/photo/low-light-photography-of-concrete-structures-419235/)

Category Page Background Image - [Photo by Startup Stock Photos from Pexels](https://www.pexels.com/photo/person-in-blue-shirt-wearing-brown-beanie-writing-on-white-dry-erase-board-7368/)
