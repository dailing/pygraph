<template>
  <g class="Box">
    <!-- draw main box -->
    <rect 
      :width="state.width" 
      :height="state.height" 
      :x="state.x"
      :y="state.y" 
      class="box"
      :class="{mouseon : mouse_on || status_mousedown, 
              selected : selected}"
      @mouseover="mouse_on=true"
      @mouseleave="mouse_on=false"
      @mousedown="mouse_down"
      @mousemove="mouse_move"
      @mouseup="mouse_up"
    />
    <g>
      <!-- draw ports -->
      <rect v-for="ii in ports"
        :key='ii.id'
        :x='ii.x - ii.isout * port_width'
        :y='ii.y'
        :width='port_width'
        :height='port_height'
        class="port"
        :class="{selected: ii.id == selected_port}"
        @click="$emit('port_click', state.uuid, ii)"
      />
      <!-- draw port texts -->
      <text v-for="ii in ports"
        :key='ii.id + "text"'
        :x='ii.x + (1-ii.isout*2) * port_width * 1.5'
        :y='ii.y + port_height'
        class="port_text"
        :class="{out: ii.isout}"
        :text-anchor="ii.isout?'end':'start'"
      >{{ii.text}}</text>
    </g>

    <g>
      <text
        :x='state.x+state.width/2'
        :y='state.y+state.height/2'
        text-anchor='middle'
      >{{state.name}}</text>
    </g>
    <rect v-if="status_mousedown"
      width='100%'
      height ='100%'
      opacity='0%'
      @mousedown="mouse_down"
      @mousemove="mouse_move"
      @mouseup="mouse_up"
    />
  </g>
</template>

<script>
export default {
  name: "Box",
  data: function() {
    return {
      mouse_on: false,
      startx: 0,
      starty: 0,
      status_mousedown: false,
      status_drag : false,
      port_size:15,
      port_width:10,
      port_height:10,
      // ports:[],
    };
  },
  methods: {
    mouse_down: function (event) {
      // console.log(event)
      this.startx = event.x;
      this.starty = event.y;
      this.ox = this.state.x;
      this.oy = this.state.y;
      this.status_mousedown = true;
      this.$emit('box_mouse_down', this.state.uuid)
      event.stopPropagation();
      return false;
    },
    mouse_move: function(event){
      if (this.status_mousedown){
        var dx = event.x - this.startx;
        var dy = event.y - this.starty;
        if(Math.abs(dx) > 10 || Math.abs(dy) > 10 || this.status_drag){
          this.state.x = this.ox + dx;
          this.state.y = this.oy + dy;
          this.status_drag = true
        }
      }
      event.stopPropagation();
      return false;
    },
    mouse_up: function(event){
      this.mouse_move(event);
      if(!this.status_drag && this.status_mousedown){
        // console.log('click');
        this.$emit('box_select', this.state.uuid);
      } else if(this.status_drag && this.status_mousedown){
        // console.log('drag');
        this.$emit('move_box', this.state.uuid);
      }
      this.status_drag = false;
      this.status_mousedown = false;
      event.stopPropagation();
      return false;
    },
  },
  props: {
    state: {
      type: Object,
      required: true
    },
    selected: {
      type:Boolean,
      required: false,
      default: false,
    },
    selected_port: {
      type: String,
      required:false,
      default:null,
    }
  },
  computed:{
    ports: function(){
      // make input ports
      var self_use=[];
      for(let i=0; i < this.state.num_input_args; i+=1){
        self_use.push({
          x:this.state.x,
          y:this.state.y+(i+0.5)*this.port_size,
          width:this.port_width,
          height:this.port_height,
          text:'args_' + i,
          id:this.state.uuid + '.input.args.'+i,
          isout:false,
        });
      }
      for(let i=0; i < this.state.kwargs.length; i+=1){
        self_use.push({
          x:this.state.x,
          y:this.state.y+(i+0.5+this.state.num_input_args)*this.port_size,
          width:this.port_width,
          height:this.port_height,
          text:this.state.kwargs[i],
          id:this.state.uuid + '.input.kwargs.'+this.state.kwargs[i],
          isout:false,
        })
      }
      if(this.state.output_type == 'value'){
        self_use.push({
          x:this.state.x+this.state.width,
          y:this.state.y+(0+0.5)*this.port_size,
          width:this.port_width,
          height:this.port_height,
          text:'value',
          id:this.state.uuid + '.output.value.',
          isout:true,
        })
      } else if (this.state.output_type == 'list'){
        for(let i=0; i < this.state.output_list_number; i+=1){
          self_use.push({
            x:this.state.x + this.state.width,
            y:this.state.y+(i+0.5)*this.port_size,
            width:this.port_width,
            height:this.port_height,
            text:'out_'+i,
            id:this.state.uuid + '.output.list.'+i,
            isout:true,
          })
        }
      } else if (this.state.output_type == 'dict'){
        for(let i=0; i < this.state.output_keywords.length; i+=1){
          self_use.push({
            x:this.state.x + this.state.width,
            y:this.state.y+(i+0.5)*this.port_size,
            width:this.port_width,
            height:this.port_height,
            text:this.state.output_keywords[i],
            id:this.state.uuid + '.output.dict.'+this.state.output_keywords[i],
            isout:true,
          }) 
        }
      }
      // this.ports = self_use;
      var convert_dict = {}
      for(var xx of self_use){
        convert_dict[xx.id] = xx;
      }
      this.$emit('box_port_change',this.state.uuid, convert_dict);
      return convert_dict;
    }
  },
  created: function(){
    // console.log('created');
    // this.calculate_ports();
  },
};
</script>

<style scoped>
rect.box {
  fill: cornflowerblue;
  opacity: 60%;
}
rect.box.selected {
  stroke:tomato;
  stroke-width: 3;
}
rect.box.mouseon {
  fill: darkblue;
}
rect.port{
  fill:darkslategrey;
}
rect.port.selected {
  stroke: tomato;
  stroke-width: 3;
}
text {
  pointer-events: none;
}
text.port_text{
  font-size: 10pt;
}


</style>