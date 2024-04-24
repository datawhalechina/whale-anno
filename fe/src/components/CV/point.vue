<template>
  <div class="anno-img-box">
    <div class="point-box">
      <img class="anno-img" id="anno-img" @click="addPoint($event)" :src="`data:image/jpeg;base64,${fileContent}`" @dragstart="$event.preventDefault()" @contextmenu="$event.preventDefault()">
      <div v-for="annoDetail in annoDetails" :point="annoDetail" :key="`${annoDetail.points[0][0]}_${annoDetail.points[0][1]}`" :style="{
        left: annoDetail.points[0][0]*100 + '%',
        top: annoDetail.points[0][1]*100 + '%',
        backgroundColor: types[annoDetail.type]?types[annoDetail.type].color:'#f00',
      }" class="point" @contextmenu="$event.preventDefault();delPoint(annoDetail, true)" @touchstart="$event.preventDefault();delPoint(annoDetail, false)" @mouseover="overPoint($event, annoDetail)"></div>
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
    },
    addPoint (ev) {
      ev.preventDefault()
      if (!this.nowType) {
        alert('请先选择标注类型')
        return
      }
      const tar = ev.target
      const newPoint = [ev.offsetX / tar.offsetWidth, ev.offsetY / tar.offsetHeight]
      // this.points.push(newPoint)
      // console.log(this.points)
      this.annoDetails.push({
        points: [newPoint],
        type: this.nowType
      })
      this.save()
      return false
    },
    delPoint (annoDetail, isForce) {
      if (!isForce) {
        // 非强制删除，就判定下当前类型是否一致，不一致就不删除
        if (this.nowType !== annoDetail.type) {
          return
        }
      }
      const idx = this.annoDetails.indexOf(annoDetail)
      console.log(annoDetail, this.points)
      this.annoDetails.splice(idx, 1)
      this.save()
    },
    overPoint (ev, point) {
      if (ev.which === 3) {
        this.delPoint(point)
      }
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
.point-box {
  width: 400px;
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
