const COLORS = [
  '#e12d2d', // 红
  '#f5a314', // 橙
  '#fff838', // 黄
  '#72ca2b', // 绿
  '#529dff', // 蓝
  '#647cf7', // 靛
  '#a855ec', // 紫
  '#eb98de', // 粉
  '#c08c8e', // 褐
  '#d2ff8f' // 青
]

function getColor (types = {}) {
  const alreadyColorDic = {}
  Object.keys(types).forEach(type => {
    const { color } = types[type]
    alreadyColorDic[color] = true
  })
  const remainingColors = []
  COLORS.forEach(color => {
    if (!alreadyColorDic[color]) remainingColors.push(color)
  })
  if (remainingColors.length) {
    // 优先选用未选择的初始颜色
    const idx = Math.random() * remainingColors.length | 0
    return remainingColors[idx]
  } else {
    const idxs = '0123456789abcdef'
    let color = '#'
    for (let i = 0; i < 6; i += 1) {
      color += idxs[Math.random() * idxs.length | 0]
    }
    return color
  }
}

export {
  getColor
}
