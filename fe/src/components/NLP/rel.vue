<template>
  <div class="rel-box">
    <svg v-for="(relLine, idx) in relLines" :key="idx" class="rel"
        xmlns="http://www.w3.org/2000/svg" version="1.1" >
      <marker id="arrow" markerUnits="strokeWidth" markerWidth="8" markerHeight="8" viewBox="0 0 12 12" refX="6" refY="6" orient="auto">
        <path d="M2,2 L10,6 L2,10 L6,6 L2,2" :style="`fill:${types[relDetails[idx]['type']]['color']}`"/>
      </marker>
      <path :d="relLine"
        :title="relDetails[idx]['type']"
        :style="`stroke:${types[relDetails[idx]['type']]['color']};stroke-width:3;fill:#0000;marker-end:url(#arrow)`"
        @contextmenu="delRel($event, idx)"
      />
    </svg>
  </div>
</template>

<script>
export default ({
  name: 'Rel',
  props: {
    nowType: {
      type: String,
      default: '1234',
      required: true
    },
    relDetails: {
      type: Array,
      required: true
    },
    save: {
      type: Function,
      required: true
    },
    types: {
      type: Object,
      required: true
    }
  },
  data () {
    return {
      points: [],
      width: 0,
      height: 0,
      relLines: []
    }
  },
  methods: {
    log (...args) {
      console.log(args)
    },
    delRel (e, idx) {
      e.preventDefault()
      this.relDetails.splice(idx, 1)
      this.save()
    },
    calRelLines (val) {
      console.log('21341234');
      if (!val) {
        val = this.relDetails
      }
      console.log(this.types)
      let _relLines = []
      for (let i = 0; i < val.length; i++) {
        const item = val[i]
        let startCharDom = document.getElementById(item.start)
        let endCharDom = document.getElementById(item.end)
        let sx = startCharDom.offsetLeft + startCharDom.offsetWidth / 2
        let sy = startCharDom.offsetTop + 9
        let ex = endCharDom.offsetLeft + endCharDom.offsetWidth / 2
        let ey = endCharDom.offsetTop + 9
        let cx = (sx + ex) / 2
        let cy = (sy + ey) / 2 - 20
        _relLines.push(`M${sx} ${sy} Q${cx} ${cy} ${ex} ${ey}`)
      }
      console.log(_relLines)
      this.relLines = _relLines
    }
  },
  watch: {
    relDetails: {
      handler (val) {
        this.calRelLines(val)
      },
      deep: true
    },
    nowType: {
      handler (val) {
      }
    }
  },
  mounted () {
    let that = this
    window.onresize = function () {
      that.calRelLines()
    }
  }
})
</script>

<style scoped>
  .rel-box,
  .rel {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 100;
    /* background: rgba(0, 0, 0, 0.5); */
    pointer-events: none;
  }
  .rel path {
    pointer-events: all;
    cursor: pointer;
  }
  .rel:hover {
    /* 抬起来一些 */
    opacity: 0.5;
  }
</style>
