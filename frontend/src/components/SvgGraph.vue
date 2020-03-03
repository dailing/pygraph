<template>
  <svg v-bind:width="width" v-bind:height="height">
    <Box 
      v-for="(b, index) in boxes"
      :state="b"
      :id="index"
      :key="index"
      @select="box_selection"
    />
  </svg>
</template>

<script>
import Box from "./Box.vue";

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
      type: Array,
      required: true
    }
  },
  components: {
    Box
  },
  methods: {
    box_selection: function(boxid) {
      console.log(boxid);
    }
  }
};
</script>

<style scoped>
</style>