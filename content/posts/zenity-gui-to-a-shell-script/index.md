---
title: 'Zenity GUI to a Shell Script'
date: 2007-10-21T20:30:00.002+10:00
draft: false
url: /2007/10/zenity-gui-to-shell-script_5432.html
tags: 
- zenity
- gui
- linux
- articles
- python
---

  
[![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEigBFNcFKSB9lKhJPiSiwDlp9q9SmO2yEu9v343B1M-2NFN5s2cJ-cUji8qR3LW1CmmitKztwUh3QxLAIjkSMYio5lIwhX1GszzhfZnufjrxugrWTNSZLH06e-qxV4ldttqBMDRBPWfXlc4/s800/zenityss.jpg)](http://picasaweb.google.com/lh/photo/whbV2vHNOr5d7pvO8qsgRw?feat=embedwebsite)  
  

I have to admit, I'm pretty lazy. I don't (ironically) like to type, and I really don't like typing the same command over and over. I found myself switching between my external monitor and laptop quite frequently, and decided to somewhat automate the task. Although I know there are other programs out there that allow this, they either had too many features, or crashed. Xrandr works just fine, but like I said, I'm lazy...

Enter [Zenity](http://live.gnome.org/Zenity). Initially I created a PyGTK monitor switcher, yet wanted something even simpler. If you aren't in the know, Zenity allows you to create super fast, super simple dialogs to regular commands. After you click "ok", the command is executed, and the dialog disappears. Perfect for switching displays.

And here is the simplistic code behind it:

```
#!/bin/sh

ans=$(zenity  --list  --text "How do you want to switch your monitor?" \\
--radiolist  --column "Pick" --column "Output Type" TRUE LCD FALSE VGA \\
FALSE Both);

if \[ "$ans" = "LCD" \]
then
xrandr --output VGA --off
xrandr --output LVDS --auto
elif \[ "$ans" = "VGA" \]
then
xrandr --output LVDS --off
xrandr --output VGA --auto
elif \[ "$ans" = "Both" \]
then
xrandr --output VGA --auto
xrandr --output LVDS --mode 1024x768
fi



```  
  

I send a big cheers and thanks to the Zenity guys, I'll surely use this quick language more frequently.