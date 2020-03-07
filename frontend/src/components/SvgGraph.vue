<template>
  <div class="columns">
    <div class="column">
      <b-collapse aria-id="wtf_1" class="panel">
        <div slot="trigger" class="panel-heading" role="button" aria-controls="wtf_1">
          <strong>box property</strong>
        </div>
        <!-- <p class="panel-tabs">
          <a class="is-active">All</a>
          <a>Public</a>
          <a>Private</a>
        </p>-->
        <div class="panel-block" v-if="selected_box!=null">
          <section>
            <b-field label="Name">
              <b-input v-model="boxes[current_box].name"></b-input>
            </b-field>

            <b-field label='#args:'>
               {{boxes[current_box].num_input_args}} 
              <b-button @click="boxes[current_box].num_input_args -= 1">-</b-button>
              <b-button @click="boxes[current_box].num_input_args += 1">+</b-button>
            </b-field>
            <b-field label='kwargs:'>
               <table>
                 <tr v-for="(k, idx) in boxes[current_box].kwargs" :key="k">
                   <td>{{k}}</td>
                   <td><b-button @click="boxes[current_box].kwargs.splice(idx,1)">del</b-button></td>
                 </tr>
                 <tr>
                   <td><b-input v-model="new_kwargs"></b-input></td>
                   <td><b-button @click="boxes[current_box].kwargs.push(new_kwargs); new_kwargs=null">add</b-button></td>
                 </tr>
               </table>
            </b-field>

          </section>
        </div>
      </b-collapse>
    </div>
    <div class="column is-three-quarters">
      <svg 
        v-bind:width="width" v-bind:height="height"
      >
        <g
            @mousemove="mouse_move"
        >
          <rect class="outer_box"
            width='100%'
            height='100%'
            @click="cancel_select"
          />
        </g>
        <Wire v-for="w in wires" :key="w.uuid" :wire="w" :ports="ports" />
        <Box
          v-for="(b) in render_list"
          :state="boxes[b]"
          :selected="b == selected_box"
          :selected_port="selected_port == null? null : selected_port.id"
          :key="boxes[b].uuid"
          @box_mouse_down="box_mouse_down"
          @box_port_change="box_port_change"
          @box_select="box_select"
          @port_click="port_click"
        />
        <!-- <g class="temp_wire" v-if="selected_port!=null">
          <path
            :d="temp_wire_path"
          />
        </g> -->
      </svg>
    </div>
  </div>
</template>

<script>
import Box from "./Box.vue";
import Wire from "./Wire.vue";

export default {
  name: "SvgGraph",
  props: {
    width: {
      type: [String, Number],
      default: "100%"
    },
    height: {
      type: [String, Number],
      default: 600
    },
    boxes: {
      type: Object,
      required: true
    },
    wires: {
      type: Object,
      required: true
    }
  },
  components: {
    Box,
    Wire
  },
  data: function() {
    return {
      ports: {},
      current_box: null,
      selected_box: null,
      new_kwargs:null,
      selected_port:null,
      selected_port_box:null,
      current_mouse:null,
    };
  },
  methods: {
    box_mouse_down: function(boxid) {
      // console.log(boxid);
      this.current_box = boxid;
      // this.$set(this, "current_box", boxid);
    },
    box_port_change: function(uuid, ports) {
      // let tmp = {};
      // for (let ii of ports) {
      //   tmp[ii.id] = ii;
      // }
      this.$set(this.ports, uuid, ports);
      // this.ports[uuid] = tmp;
    },
    box_select: function(boxid) {
      // console.log(boxid);
      this.selected_box = boxid;
    },
    test_method: function(event) {
      console.log(event)
    },
    port_click: function(boxid, port) {
      // console.log(boxid);
      // console.log(port);
      if(this.selected_port == null){
        this.selected_port = port;
        this.selected_port_box = boxid;
      } else {
        var input_port = this.selected_port.isout? port: this.selected_port;
        var output_port = input_port == port? this.selected_port: port;
        input_port = input_port.id.split('.');
        output_port = output_port.id.split('.');
        console.log(output_port);
        var wire = {
          output_from_node_uuid:output_port[0],
          output_from_node_output_type:output_port[2],
          output_from_node_output_key:output_port[2]=='dict'?output_port[3]:"",
          output_from_node_output_index:output_port[2]=='list'?parseInt(output_port[3]):0,
          input_to_node_uuid:input_port[0],
          input_to_node_input_type:input_port[2],
          input_to_node_input_key:input_port[2]=='kwargs'?input_port[3]:"",
          input_to_node_input_index:input_port[2]=='args'?parseInt(input_port[3]):0,
          uuid:'asdfasdfasdf', // TODO: make this correct
        }
        this.wires[wire.uuid] = wire;
        this.selected_port = null;
        this.selected_port_box = null;
        console.log(wire)
      }
    },
    cancel_select(){
      // console.log('cancel');
      // console.log(e);
      this.selected_port_box = null;
      this.selected_port = null;
      this.selected_box = null;
    },
    mouse_move: function(event){
      this.current_mouse = {x:event.x, y:event.y}; 
      // console.log(event);
    },
  },
  created() {},
  computed: {
    render_list: function() {
      var l = [];
      if (this.current_box != null) {
        l.push(this.current_box);
      }
      for (var x in this.boxes) {
        if (x != this.current_box) {
          l.push(x);
        }
      }
      return l.reverse();
    },
    temp_wire_path(){
      if(this.selected_port == null){
        return '';
      }
      var delta = this.selected_port.isout? 40: -40;
      var path = 'M ' + this.selected_port.x + ' ' + this.selected_port.y + ' ' +
        'C ' + (this.selected_port.x + delta) + ' '+ this.selected_port.y + ' ' +
        (this.current_mouse.x - delta) + ' ' + (this.current_mouse.y) + ' ' + 
        this.current_mouse.x + ' ' + this.current_mouse.y;

      return path;
    },
  }
};
</script>

<style scoped>
.outer_box {
  fill: thistle;
}
.temp_wire {
  fill:none;
  stroke: black;
  stroke-width: 2;
}
</style>