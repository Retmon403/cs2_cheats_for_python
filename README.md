# cs2_cheats_for_python
https://www.youtube.com/watch?v=tEKdBr8zF08  
  
适用于中国宝宝体质的cs2作弊  
以前是以前，现在是现在  
狗鑫：开了就是开了？  

# 功能
1.EspBox  
2.EspBons  
3.Esp player name/weapon  
4.EspEntity/WeaponItems  
5.Aimbot  
6.Rcs  
7.Trigger  
8.Bhop  
9.Adjustable parameters  

# 如何运行
 拥有Python 64bit环境  
你还需要[pip install ...] 一些关键模块  
1.pip install pymem  
2.pip install pywin32  
3.pip install ctypes  
4.pip install pyimgui   
5.pip install pyglet  
  
为什么要使用ImGui画窗口却用GDI绘制？  
咱老北京儿人没别的，您猜怎么着？诶，就是这一出~  

1. pip install pymem  
2. pip install pywin32  
3. pip install ctypes  
4. pip install pyimgui  
5. pip install pyglet  

# 更新日志
2023/12/7  
英语很烂，所以变量和函数命名比较随意，但代码逻辑还是很精简的  
1.很努力的优化gdi让他可以流畅的绘图而不会出现闪框  
2.加入了平滑自瞄,加入了自动更新offset  
3.优化了运行效率,修了一些bug  
还想加许多功能，但我担心Python跑起来太卡  
2023/12/7  
English is terrible, so variable and function names are quite casual, but the code logic is still very concise  
1. He worked very hard to optimize GDI so that he could draw smoothly without flashing frames  
2. Added smooth self aiming and automatic update offset  
3. Optimized operational efficiency and fixed some bugs  
I still want to add many functions, but I'm worried that Python will run too laggy  
_____________________________________________   
2024/2/20  
修复了偏移定位使用的特征码  
使用了最新的cs2dump client偏移数据  
增加了连跳和自动扳机  
添加了瞄准部位选项  
offset在成功获取到后会被储存进文件  
一些bug修复和性能优化  
2024/2/20  
Fixed feature codes used for offset positioning  
Using the latest cs2dump client offset data  
Added combos and automatic triggers  
Added targeting location option  
After successfully obtaining the offset, it will be stored in a file  
Some bug fixes and performance optimizations  
_____________________________________________  
2024/2/21  
增加了EspInfo(player_weapon,player_name,player_health)  
增加了rcs抑制控制滑块  
增加了trigger持续时间控制滑块  
修复了trigger效率问题  
一些bug修复和性能优化  
ps：感谢大家的使用,如果您需要自己修改偏移量，只需修改client.py内的内容 并将UPDATE_OFFSET设置为false，再修改offset_config文件内的偏移  
February 21, 2024  
Added EspInfo (player_weapon, playername, player_health)  
Added RCS suppression control slider  
Added trigger duration control slider  
Fixed trigger efficiency issue  
Some bug fixes and performance optimizations  
PS: Thank you for using it. If you need to modify the offset yourself, just modify the content in client.py and set UPDATE-OFFSET to false, then modify the offset in the offset_config file  
_____________________________________________  
2024/2/22  
Entity增加显示掉落物实体，穷举遍历非常影响性能  
更好的连跳  
性能优化  
February 22, 2024  
Increasing the display of dropped object entities and exhaustive traversal greatly affects performance  
Better continuous jumping  
performance optimization  

_____________________________________________  
2024/8/27  
大家过的还好吗，这个夏天非常热  
由于这是外部，py也无法编译dll，所以我想加入些更变态的功能很困难，比如hook input内的函数...  
更新了偏移量，优化了代码  
2024/8/27  
Are you all doing well? This summer is very hot  
Since this is external and py cannot compile DLLs, it is difficult for me to add some more abnormal features, such as functions inside hook input  
Updated offset and optimized code  
# 问题
你是不是想问我，运行起来为什么这么卡？  答：用易语言就不会卡  
为什么不用c++，却用python？  答：因为python写起来简单，代码量比c++少一万倍  
如何更新offset?  答：main.py中 变量->UPDATE_OFFSET默认为TRUE 程序会自动更新偏移量  
How to update offset?  
Answer: Variable ->UPDATE in main.py_ OFF SET defaults to true and the program will automatically update the offset  
# 你好，搞男童了解一下？
同性交友群:707649195  
# 截图
https://www.youtube.com/watch?v=tEKdBr8zF08  
  
![image](https://github.com/Retmon403/cs2_cheats_python/blob/main/1.png)
![image](https://github.com/Retmon403/cs2_cheats_python/blob/main/3.gif)
![image](https://github.com/Retmon403/cs2_cheats_python/blob/main/2.png)

# LICENSE
MIT License

Copyright (c) 2023 mmxx

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
