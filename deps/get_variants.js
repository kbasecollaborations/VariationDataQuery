chr = process.argv[2]
start = process.argv[3]
stop = process.argv[4]
url_template = process.argv[5]
tbi_url_template = process.argv[6]
index = process.argv[7]
//console.log(url_template)
//console.log(chr + "\t"+ start +"\t" + stop)

fs = require('fs')
const { TabixIndexedFile } = require("@gmod/tabix");
const VCF = require("@gmod/vcf");
const {RemoteFile} = require('generic-filehandle')
const remoteTbiIndexed = new TabixIndexedFile({
  filehandle: new RemoteFile(url_template),
  tbiFilehandle: new RemoteFile(tbi_url_template) // can also be csiFilehandle
})
const lines = []
async function getvar(){
await remoteTbiIndexed.getLines(chr, start, stop, (line, fileOffset) => lines.push(line))


fs.writeFile('/kb/module/work/tmp/data'+index+'.txt', lines, function (err,data) {
  if (err) {
    return console.log(err);
  }
});

const headerText = await remoteTbiIndexed.getHeader()
const tbiVCFParser = new VCF({ header: headerText })

fs.writeFile('/kb/module/work/tmp/sample_names'+index+'.txt', tbiVCFParser.samples, function (err,data) {
  if (err) {
    return console.log(err);
  }
  //console.log(tbiVCFParser.samples);
});
}

getvar()


