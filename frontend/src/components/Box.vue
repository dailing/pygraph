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
  }
};
</script>

<style scoped>
rect.box {
  fill: cornflowerblue;
}
rect.box.mouseon {
  fill: darkblue;
}
</style>