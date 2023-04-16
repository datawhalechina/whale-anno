<template>
  <div class="rel-box">
    <div v-for="(relDetail, idx) in relDetails" :key="idx" class="rel" @click="clickLine(idx)">
      <div>{{relDetail}}</div>
    </div>
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
      default: undefined,
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
    relDetails: {
      handler (val) {
        console.log(val)
      },
      deep: true
    },
    delRel: {
      handler (val) {
        if (!val) {
          return
        }
        this.relDetails.splice(this.relDetails.indexOf(val), 1)
        this.save()
      }
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
</style>
