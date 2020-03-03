<template>
  <g class="Box">
    <rect 
      :width="state.width" 
      :height="state.height" 
      :x="state.x" 
      :y="state.y" 
      class="box"
      :class="{mouseon : mouse_on}"
      @click="$emit('select', id)"
      @mousemove="mouse_on=true"
      @mouseleave="mouse_on=false"
    />
  </g>
</template>

<script>
export default {
  name: "Box",
  data: function() {
    return {
      mouse_on: false
    };
  },
  methods: {
    on_click: function () {
      console.log('click');
    }
  },
  props: {
    state: {
      type: Object,
      required: true
    },
    id: {
      type: Number,
      required: true
    }
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