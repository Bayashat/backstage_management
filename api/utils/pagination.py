"""
This is my custom paging component, if you want to use this paging component, you need to do the following

in the view function:

    def ViewFunc(request):

        #   1. Filter your own data according to your own situation
        queryset = models.VipNum.objects.all()

        #   2. Instantiate the pagination object
        page_obj = Pagination(request, queryset)

        # page_queryset = page_obj.page_queryset
        # page_str = page_obj.html()

        context = {
            "data_list": page_obj.page_queryset,  # Paged data
            "page_str": page_obj.html()  # Generate page html
        }
        return render(request, 'template.html', context)

in the HTML page:

    {% for obj in data_list %}
        {{ obj.xx }}
    {% endfor %}

    <div>
        <ul class="pagination">
                {{ page_str }}
        </ul>
    </div>
        
""" 
from django.utils.safestring import mark_safe

class Pagination(object):
    def __init__(self, request, queryset, page_size=10, page_param="page", plus=5):
        """
        :param request: object of request
        :param queryset: Eligible data (based on this data to paginate it)
        :param page_size: How many pieces of data to display per page
        :param page_param: Parameters passed in the URL to obtain pagination, for example: /app01/vipnum/list/?page=5
        :param plus: Display the previous or next few pages (page number) of the current page
        """
        # Solve the pagination problem with search box
        import copy
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict

        page = request.GET.get(page_param, '1')
        if page.isdecimal():  # Determine whether the page is a decimal number
            page = int(page)
        else:
            page = 1

        self.page = page  # Current page
        self.page_size = page_size  # The number of data items displayed on each page
        self.page_param = page_param
        self.start = (page - 1) * page_size  # Starting point
        self.end = page * page_size  # Ending point

        self.page_queryset = queryset[self.start: self.end]  # filtered data

        total_count = queryset.count()  # Total number of data

        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count += 1

        self.total_page_count = total_page_count  # total number of pages
        self.plus = plus  

    def html(self):
        if self.total_page_count <= 2*self.plus:  # When the amount of data is small, only the number of pages within 10 pages can be displayed
            start_page = 1
            end_page = self.total_page_count + 1
        else:  # The database has a lot of data, > 10 pages
            # Judge the current page
            if self.page <= self.plus:  # Current page<5 (small extreme value)
                start_page = 1
                end_page = 2 * self.plus + 1
            else:  # current page>5
                start_page = self.page - self.plus
                if self.page + self.plus > self.total_page_count:  # Can not current page+5 > total page number
                    end_page = self.total_page_count + 1  # Take before and don't take after
                else:
                    end_page = self.page + self.plus + 1

        #   2.5) page number:
        page_list = []


        self.query_dict.setlist(self.page_param, [1])
        # print(self.query_dict.urlencode())  # q=7&page=1

        #   2.6) front page
        prev = "<li><a href='?{}'>First Page</a></li>".format(self.query_dict.urlencode())
        page_list.append(prev)

        #   2.7) previous page
        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page - 1])
            prev = "<li><a href='?{}'>«</a></li>".format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [1])
            prev = "<li class='disabled'><a href='?{}'>«</a></li>".format(self.query_dict.urlencode())
        page_list.append(prev)

        #   page number:
        for i in range(start_page, end_page):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_list.append(ele)

        #   2.8) next page
        if self.page < self.total_page_count:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            prev = "<li><a href='?{}'>»</a></li>".format(self.query_dict.urlencode())
            page_list.append(prev)
        else:
            self.query_dict.setlist(self.page_param, [self.total_page_count])
            prev = "<li class='disabled'><a href='?{}'>»</a></li>".format(self.query_dict.urlencode())
            page_list.append(prev)

        #   2.9) last page
        self.query_dict.setlist(self.page_param, [self.total_page_count])
        next = "<li><a href='?{}'>Last Page</a></li>".format(self.query_dict.urlencode())
        page_list.append(next)

        searching_page = """    
        <li>
            <form action="" method="get" style="float: left; margin-left: 10px">
                <input name="page" style="position: relative; float: left; width: 120px; border-radius: 0;"
                        type="text" class="form-control" placeholder="Page Number">
                <button style="border-radius: 0" class="btn btn-default" type="submit">Redirect</button>     
            </form>
        </li>
        """
        page_list.append(searching_page)

        page_str = mark_safe("".join(page_list))

        return page_str
