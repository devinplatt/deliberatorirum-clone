// Avoid template delimiter conflicts
// (both vue.js and flask jinja2 use {{, }})
Vue.config.delimiters = ['(%', '%)'];
//console.log(Vue.config)

// demo data
/*var data = {
  title: 'My Tree',
  description: 'thing',
  children: [
    { title: 'hello', description: 'thing2' },
    { title: 'wat', description: 'thing3' }
  ]
}*/

// registering the component first
//Vue.component('type-icon', {
//  template: '[((%model.type%))]'
//})

// define the item component
Vue.component('item', {
  template: '#item-template',
  //el: '#demo',
  // description: 'hi!',
  data: function () {
    return {
      open: false,
      details: false,
      adding: false,
      view_details: true,
      view_edit: false
    }
  },
  computed: {
    isFolder: function () {
      return this.model.children &&
        this.model.children.length
    },
    isnotFolder: function () {
      // Figure out how to call !isFolder here
      return !(this.model.children &&
        this.model.children.length);
    },
    isIssue: function () {
      return this.model.type == 'issue';
    },
    isIdea: function () {
      return this.model.type == 'idea';
    },
    isPro: function () {
      return this.model.type == 'pro';
    },
    isCon: function () {
      return this.model.type == 'con';
    },
    isDefaultType: function () {
      return this.model.type === undefined || this.model.type == 'default';
    }
  },
  methods: {
    toggle: function () {
      if (this.isFolder) {
        this.open = !this.open
      }
    },
    toggle_details: function () {
      this.details = !this.details;
      if (this.details) {
        this.view_details = true;
        this.view_edit = false;
      }
    },
    toggle_adding: function () {
      this.adding = !this.adding
      console.log(this.adding)
    },
    delete_item: function () {
      console.log(this.model.title);
      if (this.$parent.$parent !== undefined) {
        console.log(this.$parent.model.title);
        var children = this.$parent.model.children;
        //console.log(children);
        var to_remove = -1;
        for (var i = 0; i < children.length; i++) {
          //console.log(children[i].title);
          if (children[i] == this.model) {
            console.log("match!");
            to_remove = i;
            break;
          }
        }
        //console.log(to_remove);
        //console.log(children[to_remove].title);
        if (to_remove != -1) {
          // remove it
          console.log("removing :" + String(children[to_remove].title));
          children.splice(to_remove, 1);
          console.log(children);
        }
      }
    },
    changeType: function () {
      if (!this.isFolder) {
        this.model.$add('children', [])
        this.addChild()
        this.open = true
        this.details = false
        this.adding = false
      }
    },
    addChild: function () {
      this.model.children.push({
        title: 'new stuff',
        description: 'new description',
        type: 'default'
      })
    },
    switch_to_edit: function () {
      this.view_edit = true;
      this.view_details = false;
    },
    switch_to_details: function () {
      this.view_details = true;
      this.view_edit = false;
    },
    // polymorphism would be nice for the addIssue, addIdea, ... functions
    addItem: function (post_type) {
      if (!this.model.children) {
        this.model.$add('children', []);
      }
      this.model.children.push({
        title: 'new ' + post_type,
        description: 'new description',
        type: post_type
      });
      this.open = true;
    },
    addIssue: function () {
      this.addItem('issue');
    },
    addIdea: function () {
      this.addItem('idea');
    },
    addPro: function () {
      this.addItem('pro');
    },
    addCon: function () {
      this.addItem('con');
    }
  }
});

function foo(description) {console.log('post tree succeeds! Response: ')};

Vue.component('savebutton', {
  template: '#save-template',
  methods: {
    save: function () {
      console.log('save clicked!');
      // Copying the filter method from vue.js
      // see https://github.com/yyx990803/vue/blob/0df318c29d7e10bfa8e5c7ca31837af91ff3174c/src/filters/index.js
      // see also: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/stringify
      var tree = JSON.stringify(this.$parent.treeData, null, 2);
      console.log(tree);

      //var mapname = 'map1';
      var mapname = this.$parent.treeData.mapname;
      console.log(mapname);

      msg = '{\"mapname\": \"' + mapname + '\",\n\"tree\": ' + tree + '\n}';
      console.log(msg);

      $.ajax({
        type: "POST",
        url: "/set_tree",
        data: msg,
        success: function(description){console.log("post tree succeeds! Response: " + String(description))},
        //success: foo,
        //dataType: "json"
        //contentType: "text"  // sending
        //dataType: "json"        // receiving from server
      })
        .done(function( description ) {
          console.log("post done");
      });
    }
  }
});

// boot up the demo
/*var demo = new Vue({
  el: '#demo',
  data: {
    treeData: data,
    description: 'this'
  }
})*/

var demo = null;
var data = null;
// Callback function
function boot_demo(json_string, textStatus, jqXHR) {
  console.log('In boot_demo callback function!');
  console.log(json_string);
  data = json_string;
  if (demo === null) {
    demo = new Vue({
      el: '#demo',
      data: {
        treeData: data,
        description: 'this'
      }
    });
  } else {
    console.log('already loaded!');
    console.log(data);
    console.log(demo);
    console.log(demo.$data);
    console.log(demo.$data.treeData);
    //demo.treeData.$set(0, { childMsg: 'Changed!'})
  }
};

// Boot up the demo when we receive tree data
//$.ajax({
//  dataType: "json",
//  url: "/get_tree",
//  success: boot_demo
//});

Vue.component('load_select_button', {
  template: '#load-template',
  methods: {
    load: function () {
      console.log('load clicked!');
      var map = this.$parent.selected;
      //var map = "{\n  \"map\": \"" + this.$parent.selected + "\"\n}";
      //map = JSON.stringify(map, null, 2);
      console.log(map);
      $.ajax({
        url: "/get_tree",
        data: map,
        success: boot_demo
      });
    },
    update_maps: function (json_string, textStatus, jqXHR) {
      console.log('updating maps');
      loader_data = json_string;
      console.log(loader_data);
      console.log(this.$parent.maps);
      // this.$parent.maps.$add(, []);
      //this.model.$add('children', []);
      // console.log(this.$parent.maps);
    },
    create: function () {
      console.log('create clicked!');
      var mapname = this.$parent.new_mapname;
      console.log(mapname);
      console.log(this.$parent.maps);
      this.$parent.maps.$add(mapname, mapname);
      $.ajax({
        url: "/create_map",
        data: mapname,
        success: this.update_maps
      });
    }
  }
});

//loader = new Vue({
//  el: '#loader',
//  data: {
//    description: 'this',
//    val: 3
//  }
//});

var loader = null;
var loader_data = null;
// Callback function
function show_loader(json_string, textStatus, jqXHR) {
  console.log('In show_maps callback function!');
  //console.log(json_string);
  loader_data = json_string;
  loader = new Vue({
    el: '#loader',
    data: {
      description: 'this',
      val: 3,
      maps: loader_data,
      selected: "none",
      new_mapname: "none"
    }
  });
};

// Get the list of maps
$.ajax({
  dataType: "json",
  url: "/get_maps",
  success: show_loader
});

function load(mapid) {
  console.log('loading map');
  console.log(mapid);
  $.ajax({
    url: "/get_tree",
    data: mapid,
    success: boot_demo
  });
}
