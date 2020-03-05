<template>
<g class="wire">

</g>
</template>

<script>
export default {
    name: "Wire",
    props:{
        wire: {
            type:Object,
            reqiured: true,
        }
    },
    methods:{

    },
    data: function(){
        return {};
    },
    created: function(){
        console.log('_create wire');
        // this.$emit('wire_crete', None);
    }
}
</script>