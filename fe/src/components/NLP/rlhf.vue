<template>
  <div class="rlhf-box">
    <div v-for="(line, idx) in fileContent.split('\n')" :key="idx" class="line" @click="clickLine(idx)">
      <template v-for="(word, idx) in line">
        <span class="word" v-if="word !== '\n'" :key="idx">{{ word }}</span>
        <br v-if="word === '\n'" :key="idx"/>
      </template>
      <span class="rank" v-if="annoDetails.indexOf(String(idx+1)) !== -1">{{annoDetails.indexOf(String(idx+1)) + 1}}</span>
    </div>
  </div>
</template>

<script>

export default ({
  name: 'RLHF',
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
    clickLine (idx) {
      let rank = String(idx + 1)
      if (this.annoDetails.indexOf(rank) === -1) {
        this.annoDetails.push(rank)
      } else {
        this.annoDetails.splice(this.annoDetails.indexOf(rank), 1)
      }
      this.save()
    }
  },
  watch: {
    annoDetails: {
      handler (val) {
        console.log(val)
      },
      deep: true
    },
    nowType: {
      handler (val) {
        if (!val) {
          return
        }
        if (this.annoDetails.indexOf(val) === -1) {
          this.annoDetails.push(val)
        } else {
          this.annoDetails.splice(this.annoDetails.indexOf(val), 1)
        }
        this.save()
      }
    }
  }
})
</script>

<style scoped>
.rlhf-box {
  display: flex;
  flex-direction: column;
}
.line {
  position: relative;
  border-bottom: 1px solid;
  min-height: 36px;
}
.line:hover {
  background-color: #eee;
}
@media screen and (max-width: 768px) {
  .line:hover {
    background-color: #fff0;
  }
}
.line>.rank {
  position: absolute;
  right: 4px;
  top: 0;
  bottom: 0;
  font-size: 36px;
  line-height: 36px;
  margin: auto;
}
.word {
  display: inline-block;
  position: relative;
  padding-bottom: 15px;
  width: 20px;
  height: 20px;
  line-height: 20px;
  vertical-align: bottom;
  box-sizing: content-box;
  text-align: center;
  font-size: 16px;
  z-index: 4;
}
</style>
