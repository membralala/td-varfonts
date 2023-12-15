from fontTools import ttLib

# me - this DAT
# par - the Par object that has changed
# val - the current value
# prev - the previous value
#
# Make sure the corresponding toggle is enabled in the Parameter Execute DAT.


def onValueChange(par, prev):
    pass


# Called at end of frame with complete list of individual parameter changes.
# The changes are a list of named tuples, where each tuple is (Par, previous value)
def onValuesChanged(changes):
    webrender = op("webrender1")
    for c in changes:
        # use par.eval() to get current value
        par = c.par
        prev = c.prev

        if par.name.startswith("Axis"):
            axis = ""
            for param in parent.VarFonts.customPars:
                if param.name.startswith("Axis"):
                    tag = param.label
                    value = param
                    axis += f"'{tag}' {value}, "
            webrender.executeJavaScript(f"""setAxis("{axis[:-2]}")""")
        elif par.name == "Text":
            text = par.eval()
            if parent().par.Breaks.eval():
                text = text.replace("\n", " ", text)
            else:
                text = text.replace("\n", "<br/>")
            webrender.executeJavaScript(f"setText('{text}')")
        elif par.name == "Breaks":
            text = parent().par.Text.eval()
            if par.eval():
                text = text.replace("\n", " ")
            else:
                text = text.replace("\n", "<br/>")
            webrender.executeJavaScript(f"setText('{text}')")
        elif par.name == "Font":
            webrender.executeJavaScript(f"setFont('{par}')")
            setFontAxis(par)
        elif par.name == "Size":
            webrender.executeJavaScript(f"setFontSize({par})")
        elif par.name == "Spacing":
            webrender.executeJavaScript(f"setLetterSpacing({par})")
        elif par.name == "Height":
            webrender.executeJavaScript(f"setLineHeight({par})")
        elif par.name == "Align":
            webrender.executeJavaScript(f"setTextAlign('{par.eval().lower()}')")
    return


def onPulse(par):
    webrender = op("webrender1")
    if par.name == "Init":
        font = parent.VarFonts.par.Font
        webrender.executeJavaScript(f"setFont('{font}')")
        setFontAxis(font, destructive=False)

        text = parent.VarFonts.par.Text
        webrender.executeJavaScript(f"setText('{text}')")

        axis = ""
        for param in parent.VarFonts.customPars:
            if param.name.startswith("Axis"):
                tag = param.label
                value = param
                axis += f"'{tag}' {value}, "
        webrender.executeJavaScript(f"""setAxis("{axis[:-2]}")""")


def onExpressionChange(par, val, prev):
    return


def onExportChange(par, val, prev):
    return


def onEnableChange(par, val, prev):
    return


def onModeChange(par, val, prev):
    return


def setFontAxis(fontFile, destructive=True):
    # Load font with fontTools and get axes
    tt = ttLib.TTFont(str(fontFile))
    axes = tt["fvar"].axes
    print(axes)
    axes_tags = [a.axisTag for a in axes]

    # clear previous axes, unless they
    for par in parent.VarFonts.customPars:
        if par.name.startswith("Axis"):
            if destructive or par.label.strip("Axis") not in axes_tags:
                par.destroy()

    customPage = parent.VarFonts.customPages[0]

    for i, ax in enumerate(axes):
        new_axis = customPage.appendInt(f"Axis{i}", label=ax.axisTag)
        new_axis.min = new_axis.normMin = int(ax.minValue)
        new_axis.max = new_axis.normMax = int(ax.maxValue)
        new_axis.default = int(ax.defaultValue)
