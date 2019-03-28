var initialCats = [
    {
        clickCount: 0,
        name: 'Tabby',
        imgSrc: "img/434164568_fea0ad4013_z.jpg",
        imgAttribution: "https://www.flicker.com/photos/bigtallguy/434164568",
        nicknames: ["Bill", "Bob", "Fred"]
    },
    {
        clickCount: 0,
        name: 'Tiger',
        imgSrc: "img/4154543904_6e2428c421_z.jpg",
        imgAttribution: "https://www.flicker.com/photos/bigtallguy/434164568",
        nicknames: ["Tigger", "Bob", "Fred"]
    },
    {
        clickCount: 0,
        name: 'Scaredy',
        imgSrc: "img/22252709_010df3379e_z.jpg",
        imgAttribution: "https://www.flicker.com/photos/bigtallguy/434164568",
        nicknames: ["Chicken", "Bob", "Fred"]
    },
    {
        clickCount: 0,
        name: 'Shadow',
        imgSrc: "img/1413379559_412a540d29_z.jpg",
        imgAttribution: "https://www.flicker.com/photos/bigtallguy/434164568",
        nicknames: ["Ghost", "Bob", "Fred"]
    },
    {
        clickCount: 0,
        name: 'Monster',
        imgSrc: "img/9648464288_2516b35537_z.jpg",
        imgAttribution: "https://www.flicker.com/photos/bigtallguy/434164568",
        nicknames: ["Frankenstein", "Bob", "Fred"]
    }
]

var Cat = function (data) {
    this.clickCount = ko.observable(data.clickCount);
    this.name = ko.observable(data.name);
    this.imgSrc = ko.observable(data.imgSrc);
    this.imgAttribution = ko.observable(data.imgAttribution);

    this.catNameCount = ko.computed(function () {
        return this.name() + "(" + this.clickCount() + ")";
    }, this);

    this.nicknames = data.nicknames;
    //this.NameList = ko.oberservableArray( [ "Bob", "Fred", "Billy" ]);


    this.level = ko.computed(function () {
        if (this.clickCount() < 6) {
            return "Newborn";
        }
        if (this.clickCount() > 5) {
            if (this.clickCount() < 11) {
                return "Teen";
            }
        }
        return "Adult";
    }, this);
}

var ViewModel = function () {
    //self always maps to ViewModel, regardless of where the data-bind is on the HTML
    var self = this;

    self.catList = ko.observableArray([]);

    initialCats.forEach(function (catItem) {
        self.catList.push(new Cat(catItem));
    });

    self.currentCat = ko.observable(self.catList()[0]);



    /* 
        this.incrementCounter = function () {
            this.currentCat().clickCount(this.currentCat().clickCount() + 1);
        };
        */
    // we changed the binding context in the HTML so add var self = this
    this.incrementCounter = function () {
        self.currentCat().clickCount(self.currentCat().clickCount() + 1);
    };

    this.setCat = function (clickedCat) {
        self.currentCat(clickedCat);
    }
}

// start the app
ko.applyBindings(new ViewModel());