<template>
  <g class="Box">
    <rect 
      :width="state.width" 
      :height="state.height" 
      :x="state.x"
      :y="state.y" 
      class="box"
      :class="{mouseon : mouse_on}"
      @click="$emit('select', state.uuid)"
      @mouseover="mouse_on=true"
      @mouseleave="mouse_on=false"
      @mousedown="mouse_down"
      @mousemove="mouse_move"
      @mouseup="mouse_up"
    />
    <g>
      <rect v-for="ii in state.num_input_args"
        :key='ii'
        :x='state.x'
        :y='state.y+ii*port_size - port_size/2'
        :width='port_width'
        :height='port_height'
        class="port"
      />
      <text v-for="ii in state.num_input_args"
        :key='"text" + ii'
        :x='state.x + port_width+5'
        :y='state.y+ii*port_size'
        class="port_text"
      >args_{{ii}}</text>
      <rect v-for="(name, ii) in state.kwargs"
        :key='name'
        :x='state.x'
        :y='state.y+(ii + state.num_input_args)*port_size + port_size/2'
        :width='port_width'
        :height='port_height'
        class="port"
      />
      <text v-for="(name, ii) in state.kwargs"
        :key='"text" + name'
        :x='state.x + port_width+5'
        :y='state.y+(ii+state.num_input_args+1)*port_size'
        class="port_text"
      >{{name}}</text>
    </g>
    <g v-if="state.output_type=='value'" text-anchor="end">
      <rect
        :x='state.x+state.width - port_width'
        :y='state.y+state.height / 2 - port_height/2'
        :width='port_width'
        :height='port_height'
        class="port"
      />
      <text
        :x='state.x+state.width - port_width - 5'
        :y='state.y+state.height / 2 + port_height/2'
        class="port_text"
      >output</text>
    </g>
    <g v-if="state.output_type=='list'" text-anchor="end">
      <rect v-for="ii in state.output_list_number"
        :key='ii'
        :x='state.x+state.width - port_width'
        :y='state.y+ii*port_size - port_size/2'
        :width='port_width'
        :height='port_height'
        class="port"
      />
      <text v-for="ii in state.output_list_number"
        :key='"text" + ii'
        :x='state.x+state.width - port_width - 5'
        :y='state.y+ii*port_size'
        class="port_text"
      >args_{{ii}}</text>
    </g>

    <g v-if="state.output_type=='dict'" text-anchor="end">
      <rect v-for="(name, ii) in state.output_keywords"
        :key='ii'
        :x='state.x+state.width - port_width'
        :y='state.y+ii*port_size + port_size/2'
        :width='port_width'
        :height='port_height'
        class="port"
      />
      <text v-for="(name, ii) in state.output_keywords"
        :key='"text" + ii'
        :x='state.x+state.width - port_width - 5'
        :y='state.y+ii*port_size + port_size'
        class="port_text"
      >{{name}}</text>
    </g>

    <g>
      <text
        :x='state.x+state.width/2'
        :y='state.y+state.height/2'
        text-anchor='middle'
      >output</text>
    </g>
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
    };
  },
  methods: {
    mouse_down: function (event) {
      console.log(event)
      this.startx = event.x;
      this.starty = event.y;
      this.ox = this.state.x;
      this.oy = this.state.y;
      this.status_mousedown = true;
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
    },
    mouse_up: function(event){
      this.mouse_move(event);
      if(!this.status_drag && this.status_mousedown){
        console.log('click');
        this.$emit('select_box', this.state.uuid);
      } else if(this.status_drag && this.status_mousedown){
        console.log('drag');
        this.$emit('move_box', this.state.uuid);
      }
      this.status_drag = false;
      this.status_mousedown = false;
      // TODO: emit some message
    }
  },
  props: {
    state: {
      type: Object,
      required: true
    },
  },
  created: function(){
    console.log('created');
  },
};
</script>

<style scoped>
rect.box {
  fill: cornflowerblue;
}
rect.box.mouseon {
  fill: darkblue;
}
.port{
  fill:darkslategrey;
}
.port_text{
  font-size: 10pt;
}
text {
  pointer-events: none;
}
</style>