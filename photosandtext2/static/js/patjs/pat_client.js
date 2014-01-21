function Gallery(name, description, type) {
    var self = this;
    self.name = name;
    self.description = description;
    self.type = ko.observable(type)
}

function GalleryViewModel() {
    var self = this;

    //This would come from a server, like a list of photos or the gallery object its self.
    self.availableTypes = [
        { typeName: "Private", owner: 'Test1'},
        { typeName: "Public", owner: 'Test2'},
        { typeName: "In-between", owner: 'Test3'}
    ];

    self.galleries = ko.obserableArray([
        new Gallery("GalleryPriv", "Private Gallery", self.availableTypes[0]),
        new Gallery("GalleryPub", "Public Gallery", self.availableTypes[1])
    ])
}

ko.applyBindings(new GalleryViewModel());