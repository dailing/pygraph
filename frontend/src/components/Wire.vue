<template>
  <g class="wire">
    <g>
      <path
        :d='dd'
      />
    </g>
  </g>
</template>

<script>
export default {
  name: "Wire",
  props: {
    wire: {
      type: Object,
      reqiured: true
    },
    ports: {
      type: Object,
      reqiured: true
    }
  },
  methods: {},
  computed: {
    dd: function() {
      let ii = this.wire;
      var out_index = '';
      if (ii.output_from_node_output_type == 'list'){
        out_index = ii.output_from_node_output_index;
      } else if(ii.output_from_node_output_type == 'dict'){
        out_index = ii.output_from_node_output_key;
      }
      // console.info(ii);
      let out_id = ii.output_from_node_uuid+'.output.' + ii.output_from_node_output_type+'.'+out_index;
      // console.info(out_id)
      // console.info(this.ports[ii.output_from_node_uuid]);
      let out_port = this.ports[ii.output_from_node_uuid][out_id];

      var in_index = '';
      if(ii.input_to_node_input_type == 'args'){
        in_index = ii.input_to_node_input_index;
      } else if(ii.input_to_node_input_type == 'kwargs') {
        in_index = ii.input_to_node_input_key;
      }
      let in_id = ii.input_to_node_uuid + '.input.' + ii.input_to_node_input_type+'.' + in_index;
      // console.log(in_id);
      // console.log(this.ports[ii.input_to_node_uuid]);
      let in_port = this.ports[ii.input_to_node_uuid][in_id]
      let oo = 'M ' + out_port.x + ' ' + out_port.y + ' ' + 
                ' C '+ (out_port.x+40) + ' ' + out_port.y + ' ' +
                (in_port.x - 40) + ' ' + in_port.y + ' '+
                + in_port.x + ' ' + in_port.y;
      // console.log(oo);
      return oo;
    }
  },
  data: function() {
    return {
      local_ports: this.ports,
    };
  },
  created: function() {
    // console.log("_create wire");
    // this.$emit('wire_crete', None);
  }
};
</script>

<style scoped>
path {
  fill:none;
  stroke: black;
  stroke-width: 2;
}
</style>