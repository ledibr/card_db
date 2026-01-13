import tkinter as tk
import tkinter.ttk as ttk

# implement and/or in text boxes later
# output text window
# search submit button bound to left click OR enter (see tutorial)
# add sort by filter
# add upload dialog!!!!!!!!!!!!!!!!

class SearchUI:
    def __init__(self):
        # TODO: implement style changes (if so desired)
        self.root = tk.Tk()
        self.root.title('Database Search')
        self.content = ttk.Frame(self.root, padding=10)
        self.content.grid(column=0, row=0, sticky=tk.NSEW)
        self.root.bind('<Return>', self.process)

        self.topleft = ttk.Frame(self.content)
        self.topleft.grid(column=0, row=0, sticky=tk.NSEW)
        ttk.Separator(self.content, orient='vertical').grid(column=1, row=0, sticky='nse', rowspan=2, pady=10, padx=10)
        self.topright = ttk.Frame(self.content)
        self.topright.grid(column=2, row=0, sticky=tk.NSEW)

        self.match = ttk.Frame(self.topleft)
        self.match.grid(column=0, row=0, sticky=tk.NSEW)
        self.operator_val = tk.StringVar()
        self.populate_match()

        self.filters = ttk.Frame(self.topleft)
        self.filters.grid(column=0, row=1, sticky=tk.NSEW)
        self.year_val = tk.StringVar()
        self.series_val = tk.StringVar()
        self.setname_val = tk.StringVar()
        self.num_val = tk.StringVar()
        self.name_val = tk.StringVar()
        self.team_val = tk.StringVar()
        self.feat_val = tk.StringVar()
        self.par_val = tk.StringVar()

        self.count_val = tk.StringVar()
        self.equal_val = tk.StringVar()
        self.count_num_val = tk.StringVar()
        self.count_frame = ttk.Frame(self.filters)
        self.count_frame.grid(column=0, row=8, sticky=tk.NSEW, columnspan=4)
        self.equal_box = None
        self.count_num = None
        self.filters.columnconfigure(5, weight=1)
        self.populate_filters()

        self.uploader = ttk.Frame(self.topright, padding=(0, 0, 0, 50))
        self.uploader.grid(column=0, row=0, sticky=tk.NSEW)
        ttk.Label(self.uploader, text='Placeholder for upload tool.', anchor='w').grid(column=0, row=0, sticky=tk.N)

        self.random = ttk.Frame(self.topright, padding=(0, 0, 0, 50))
        self.random.grid(column=0, row=1, sticky=tk.NSEW)
        ttk.Label(self.random, text='Placeholder for random card picker.', anchor='w').grid(column=0, row=0, sticky=tk.N)

        self.output = ttk.Labelframe(self.content, text='Results:')
        self.output.grid(column=0, row=1, sticky=tk.NSEW, columnspan=10)
        self.populate_output()

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.content.columnconfigure([0, 1], weight=0)
        self.content.columnconfigure(2, weight=1)
        self.content.rowconfigure('all', weight=1)
        for child in self.content.winfo_children():
            # child.columnconfigure('all', weight=1)
            # child.rowconfigure('all', weight=1)
            for grandchild in child.winfo_children():
                grandchild.grid_configure(padx=3, pady=3)
                for greatgrandchild in grandchild.winfo_children():
                    greatgrandchild.grid_configure(padx=3, pady=3)

    def populate_match(self):
        ttk.Label(self.match, text='Match', anchor='w').grid(column=0, row=0, sticky=tk.NSEW)
        ttk.Label(self.match, text='of the following fields:', anchor='w').grid(column=2, row=0, sticky=tk.NSEW)
        # operator button
        operator = ttk.Combobox(self.match, textvariable=self.operator_val, width=4)
        # operator.bind('<<ComboboxSelected>>', function)
        operator['values'] = ('all', 'any')
        operator.state(['readonly'])
        operator.set('all')
        operator.grid(column=1, row=0, sticky=tk.W)

    def populate_filters(self):
        ttk.Label(self.filters, text='Year', anchor='w', width=10).grid(column=0, row=0, sticky=tk.NSEW)
        ttk.Label(self.filters, text='Series', anchor='w').grid(column=0, row=1, sticky=tk.NSEW)
        ttk.Label(self.filters, text='Set', anchor='w').grid(column=0, row=2, sticky=tk.NSEW)
        ttk.Label(self.filters, text='Number', anchor='w').grid(column=0, row=3, sticky=tk.NSEW)
        ttk.Label(self.filters, text='Name', anchor='w').grid(column=0, row=4, sticky=tk.NSEW)
        ttk.Label(self.filters, text='Team', anchor='w').grid(column=0, row=5, sticky=tk.NSEW)
        ttk.Label(self.filters, text='Features', anchor='w').grid(column=0, row=6, sticky=tk.NSEW)
        ttk.Label(self.filters, text='Parallels', anchor='w').grid(column=0, row=7, sticky=tk.NSEW)
        # filter boxes
        year = ttk.Entry(self.filters, textvariable=self.year_val, width=40)
        series = ttk.Entry(self.filters, textvariable=self.series_val)
        setname = ttk.Entry(self.filters, textvariable=self.setname_val)
        num = ttk.Entry(self.filters, textvariable=self.num_val)
        name = ttk.Entry(self.filters, textvariable=self.name_val)
        team = ttk.Entry(self.filters, textvariable=self.team_val)
        feat = ttk.Entry(self.filters, textvariable=self.feat_val)
        par = ttk.Entry(self.filters, textvariable=self.par_val)
        year.grid(column=1, row=0, sticky=tk.EW)
        series.grid(column=1, row=1, sticky=tk.EW)
        setname.grid(column=1, row=2, sticky=tk.EW)
        num.grid(column=1, row=3, sticky=tk.EW)
        name.grid(column=1, row=4, sticky=tk.EW)
        team.grid(column=1, row=5, sticky=tk.EW)
        feat.grid(column=1, row=6, sticky=tk.EW)
        par.grid(column=1, row=7, sticky=tk.EW)

        # count options
        self.count_box()

        # submit button
        ttk.Button(self.filters, text='Submit', command=self.process, default='active').grid(column=5, row=10, sticky=tk.NSEW)

    def populate_output(self):
        # output text box
        results = tk.Text(self.output, width=100, height=15, wrap='none', state='disabled')
        results.grid(column=0, row=0, sticky=tk.NSEW)
        # scrollbars
        vert_scroll = ttk.Scrollbar(self.output, orient='vertical', command=results.yview)
        horiz_scroll = ttk.Scrollbar(self.output, orient='horizontal', command=results.xview)
        vert_scroll.grid(column=1, row=0, sticky=tk.NS)
        horiz_scroll.grid(column=0, row=1, sticky=tk.EW)
        results['yscrollcommand'] = vert_scroll.set
        results['xscrollcommand'] = horiz_scroll.set

    def count_box(self):
        ttk.Label(self.count_frame, text='Count:', anchor='w', width=10).grid(column=0, row=0, sticky=tk.NSEW)
        all_count = ttk.Radiobutton(self.count_frame, text='All', variable=self.count_val, value='all',
                                    command=self.custom_count)
        unowned_count = ttk.Radiobutton(self.count_frame, text='Unowned', variable=self.count_val, value='unowned',
                                        command=self.custom_count)
        owned_count = ttk.Radiobutton(self.count_frame, text='Owned', variable=self.count_val, value='owned',
                                      command=self.custom_count)
        custom_count = ttk.Radiobutton(self.count_frame, text='Custom', variable=self.count_val, value='custom',
                                       command=self.custom_count)
        all_count.grid(column=1, row=0, sticky=tk.W, padx=(6, 0))
        unowned_count.grid(column=2, row=0, sticky=tk.W, padx=3)
        owned_count.grid(column=3, row=0, sticky=tk.W, padx=3)
        custom_count.grid(column=4, row=0, sticky=tk.W, padx=3)
        # TODO: implement custom option functionality
        self.count_val.set('all')

        self.equal_box = ttk.Combobox(self.count_frame, textvariable=self.equal_val, width=3)
        self.equal_box['values'] = ('>', '>=', '=', '<=', '<')
        self.equal_box.state(['readonly'])
        self.equal_box.set('=')
        self.equal_box.grid(column=1, row=1, sticky=tk.E, padx=(8, 0), pady=3)
        self.equal_box.grid_remove()
        self.count_num = ttk.Entry(self.count_frame, textvariable=self.count_num_val)
        self.count_num.grid(column=2, row=1, sticky=tk.EW, columnspan=3, padx=5, pady=3)
        self.count_num.grid_remove()

    def custom_count(self):
        if self.count_val.get() == 'custom':
            self.equal_box.grid()
            self.count_num.grid()
        else:
            self.equal_box.grid_remove()
            self.count_num.grid_remove()

    def process(self, *args):
        # TODO: make the things do things!
        pass

    def run(self):
        self.root.mainloop()