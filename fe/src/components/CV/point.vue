<template>
  <div class="anno-img-box">
    <div class="point-box">
      <img class="anno-img" id="anno-img" @click="addPoint($event)" :src="`data:image/jpeg;base64,${src}`" @dragstart="$event.preventDefault()" @contextmenu="$event.preventDefault()">
      <div v-for="point in points" :point="point" :key="`${point[0]}_${point[1]}`" :style="{
        left: point[0]*100 + '%',
        top: point[1]*100 + '%',
        backgroundColor: point.color
      }" class="point" @contextmenu="$event.preventDefault();delPoint(point)" @mouseover="overPoint($event, point)"></div>
    </div>
  </div>
</template>

<script>

export default ({
  name: 'CVPoint',
  props: {
    src: {
      type: String,
      default: '',
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
    },
    addPoint (ev) {
      ev.preventDefault()
      const tar = ev.target
      const newPoint = [ev.offsetX / tar.offsetWidth, ev.offsetY / tar.offsetHeight]
      console.log(newPoint)
      this.points.push(newPoint)
      console.log(this.points)
      return false
    },
    delPoint (point) {
      const idx = this.points.indexOf(point)
      console.log(point, this.points)
      this.points.splice(idx, 1)
    },
    overPoint (ev, point) {
      if (ev.which === 3) {
        this.delPoint(point)
      }
    }
  },
  watch: {
    // src: {
    //   handler (val) {
    //     const annoImg = document.getElementById('anno-img')
    //     annoImg.src = val
    //     console.log(annoImg.width)
    //     this.width = annoImg.width
    //     this.height = annoImg.height
    //   },
    //   deep: true
    // }
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
.point-box {
  width: 300px;
  position: absolute;
  font-size: 0;
}
.point {
  position: absolute;
  width: 8px;
  height: 8px;
  transform: translateX(-50%) translateY(-50%);
  border-radius: 50%;
  background-color: #f00;
}
.point:hover {
  width: 16px;
  height: 16px;
}
</style>
