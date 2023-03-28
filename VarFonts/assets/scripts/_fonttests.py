# me - this DAT
# scriptOp - the OP which is cooking
from fontTools.varLib import mutator
from fontTools import ttLib
from fontTools.pens import svgPathPen, recordingPen, pointPen
from fontTools.misc import transform
import svgwrite



# press 'Setup Parameters' in the OP to call this function to re-create the parameters
def onSetupParameters(scriptOp):
	return 

# called whenever custom pulse parameter is pushed
def onPulse(par):
	return

def onCook(scriptOp):
	scriptOp.clear()
	tt = ttLib.TTFont("/Users/philip/Documents/TouchDesigner/Raumstaben/RAUMFONT_20230206_nat-VF.ttf")

	# gset = tt.getGlyphSet()
	# pen = svgPathPen.SVGPathPen(gset)
	# gset["A"].draw(pen)
	# print(pen.getCommands())
	print(tt.keys())

	# Access the Font axis. This can be used to generate the control faders.
	# See: https://learn.microsoft.com/en-us/typography/opentype/spec/fvar
	axes = tt["fvar"].axes
	print(
		[axis.axisTag for axis in axes],
		[axis.defaultValue for axis in axes],
		[axis.minValue for axis in axes],
		[axis.maxValue for axis in axes],
		sep="\n"
	)

	# Todo: Set the axis values so that drawing with a pen tool produces 
	# expected result. Not working so far.
	# tt["fvar"].axes[0].defaultValue = 400.0
	# print(tt["fvar"].axes[0].defaultValue)
	

	# instance = mutator.instantiateVariableFont(tt, {"wght": 400})
	gset = tt.getGlyphSet({"CODE": 500.0})
	# gset = instance.getGlyphSet()
	pen = svgPathPen.SVGPathPen(gset)
	print(type(gset["A"]))#gset["A"].isVarComposite())
	print(gset.keys()[0].isComposite())
	
	svg = svgwrite.Drawing("test.svg", size=("100%", "100%"))
	# group = svg.add(svg.g())

	svg.add(svg.path(d=pen.getCommands()))
	# print(svg.tostring())
	#svg.save(True)
	#op("text3").text = svg.tostring()
	return
