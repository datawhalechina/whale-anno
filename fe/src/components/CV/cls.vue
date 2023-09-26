<template>
  <div class="anno-img-box">
    <div class="cls-box">
      <img class="anno-img" id="anno-img" :src="`data:image/jpeg;base64,${fileContent}`">
    </div>
  </div>
</template>

<script>

export default ({
  name: 'CVPoint',
  props: {
    fileContent: {
      type: String,
      default: '',
      required: true
    },
    annoDetails: {
      type: Array,
      default: () => [],
      required: true
    },
    nowType: {
      type: String,
      default: '1234',
      required: true
    },
    types: {
      type: Object,
      default: () => {},
      required: true
    },
    save: {
      type: Function,
      required: true
    }
  },
  data () {
    return {
      points: [],
      width: 0,
      height: 0
    }
  },
  methods: {
    log (...args) {
      console.log(args)
    }
  },
  watch: {
    annoDetails: {
      handler (val) {
        // const annoImg = document.getElementById('anno-img')
        // annoImg.src = val
        // console.log(annoImg.width)
        // this.width = annoImg.width
        // this.height = annoImg.height
        console.log(val)
      },
      deep: true
    }
  }
})
</script>

<style>
.anno-img-box {
  position: relative;
  display: flex;
  height: 100%;
  align-content: center;
  justify-content: center;
}
.anno-img {
  width: 100%;
  user-select: none;
}
.cls-box {
  max-width: 100%;
  position: absolute;
  font-size: 0;
}
</style>
