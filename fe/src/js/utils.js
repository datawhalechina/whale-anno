export function saveAsFile (data, name) {
  const urlObject = window.URL || window.webkitURL || window
  const exportBlob = new Blob([data])
  const saveLink = document.createElementNS('http://www.w3.org/1999/xhtml', 'a')
  saveLink.href = urlObject.createObjectURL(exportBlob)
  saveLink.download = name
  saveLink.click()
}
