from django.core.management.base import BaseCommand
import requests, re, time, random
from amazon_niche_finder.models import Category

# Credits
# time delay https://finddatalab.com/ethicalscraping#Time_outs_and_responsive_delays
# regex for name_regex: https://stackoverflow.com/questions/9889635/regular-expression-to-return-all-characters-between-two-special-characters


class Command(BaseCommand):
    help = "Adds bestseller links to any category that has a bestseller page"

    def handle(self, *args, **kwargs):

        # Known header to work with Amazon
        header = {
            "User-Agent":
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        }
        links = Category.objects.all()

        # For the moment, this is a 2 step process. Run once with level_one_regex,
        # when done comment out level_one_regex and uncomment name_regex. Replace
        # all instances of level_one_regex with name_regex and run again.
        # This is done because the csv contains 2 versions of links that 1 pass
        # won't handle. It was a late catch in the project and there's not time
        # to work through. I don't want this to break 1 day before it's due

        # From the link provided in the import CSV, isolate the category name
        # Amazon needs to build a bestseller link
        # name_regex = r"(?<=i=).+?(?=\-intl)"

        # Level 1 Regex
        level_one_regex = r"(?<=intl_).+?(?=\&rh)"

        # From the link provided in the import CSV, isolate the ID number. In some
        # cases, there will be multiple id's that fit this regex. That will be handled
        # later.
        id_regex = r"(?<=%3A)\d+"

        for i, v in enumerate(links):
            # Link from CSV import
            old_link = v.cat_link

            # All must be true or will crash
            # and re.findall(name_regex, old_link)
            if (len(old_link) > 0 and re.findall(id_regex, old_link)
                    and re.findall(level_one_regex, old_link)
                    and v.cat_bestsellers_link == None):

                # Build in a delay so Amazon won't shut down for scraping
                start = time.time()

                # Handle if regex returns multiple id's. You want the last one.
                id = re.findall(id_regex, old_link)[-1]
                name = re.findall(level_one_regex, old_link)

                # Build New link
                new_link = f"https://amazon.com/gp/bestsellers/{name[0]}/{id}"

                # You may not need a proxy, but the link_adder function is going
                # to routinely timeout after a few hours. I believe at some point
                # amazon will ban the IP and I don't want it to be MY IP.
                # You can get free US Proxies at https://www.us-proxy.org/
                # Stick with US, port 80 proxies. Doesn't have to be https.
                s = requests.Session()
                s.proxies = {
                    "http": "http://162.144.116.103:80",
                    "http": "http://12.69.91.227:80",
                    "http": "http://216.137.184.253:80",
                }
                req = s.get(new_link, headers=header)

                # Compute delay
                delay = time.time() - start

                # Not every link in CSV will have a bestseller page. Take each CSV
                # link, build a new bestseller link and ping Amazon. If you get a
                # 200, then bestseller page exists. Add it to database, enact delay
                # and start over with next link in for loop.
                if req.status_code == 200:
                    v.cat_bestsellers_link = new_link
                    v.save(update_fields=["cat_bestsellers_link"])
                    time.sleep(random.uniform(1, 2) * delay)
                    # you can remove this if you want. It's just to see that
                    # progress is being made. This function takes a few hours
                    # to run and the print at least shows something is happening.
                    print(new_link)
                else:
                    print(req.status_code)
