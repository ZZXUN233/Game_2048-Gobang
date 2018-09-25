// JavaScript Document
	var chess=document.getElementById("canvas");//获取画布
    var context = chess.getContext("2d");//平面画笔
    var over = false;//控制权，没有结束游戏

	context.strokeStyle="#aaaaaa"
	function drawBoard()
	{
		//绘制棋盘
		for(var i=0;i<=15;i++)
		{
			
			context.beginPath();
			context.moveTo(15+30*i,15);
			context.lineTo(15+30*i,435);
			context.closePath();
			context.stroke();
			
			context.beginPath();
			context.moveTo(15,15+30*i);
			context.lineTo(435,15+30*i);
			context.closePath();
			context.stroke();
		}
	}
   drawBoard();
   start();
   
   //绘制棋子
   //function draw
   /*
   context.beginPath();
   context.arc(15,15,6,0,Math.PI*2);
   context.closePath();
   context.stroke();
   */
  
   var onStep=function(i,j,me)
   {
		context.beginPath()
		context.arc(15+30*i,15+30*j,13,0,Math.PI*2);
		context.closePath();
		context.stroke();
		var gradient=context.createRadialGradient(15+30*i,15+30*j,13,15+30*i,15+30*j,0);
		if(me)
		{
			gradient.addColorStop(0,"#0a0a0a");
			gradient.addColorStop(1,"#666666");
			//context.fillStyle="black";
		}
		else
		{
			gradient.addColorStop(0,"#d1d1d1");
			gradient.addColorStop(1,"#ffffff");
			//context.fillStyle="white";
		}
		context.fillStyle=gradient;
		context.fill();
   }
		//onStep(2,2,true);
		//onStep(1,2,false);
		//落棋子
		var me=true;
		//记录下棋的信息
		var chessborad=[];
		for(var i=0;i<15;i++)//没下上棋子的都记录为0
		{
			chessborad[i]=[];
			for(var j=0;j<15;j++)
			{
				chessborad[i][j]=0;
			}
		}
   function start()
   {
		chess.onclick=function(e)
		{
            if (over)//游戏结束
            {
                return;
            }
            if (!me)//控制权在电脑，不能点击
            {
                return;
            }
			var x=e.offsetX;//27
			var y=e.offsetY;//26
			var i=Math.floor((x)/30);//0
			var j=Math.floor((y)/30);//0
			console.log(x+","+y);
			console.log(i+","+j);
			if(chessborad[i][j]==0)//有值就不能再下
            {
                /********人机对战的判断********/
                onStep(i, j, me);
                chessborad[i][j] = 1;
                for (var k = 0; k < count; k++)
                {
                    if (wins[i][j][k])
                    {
                        myWin[k]++;//第k种赢法中我们落了子
                        computerWin[k] = 0;//这种赢法下计算机就不可以赢
                        if (myWin[k] == 5)
                        {
                            alert("你赢了");
                            over = true;
							//window.location.reload();
                        }
                    }
                }
                if (!over)
                {
                    me = !me;
                    computerAi();
                }
                /*********************/
				/*if(me)
				{
					onStep(i,j,me);
					chessborad[i][j]=1;//黑棋为1
					
				}
				else
				{
					onStep(i,j,me);
					chessborad[i][j]=2;//白棋为2
				}*/
				
			}
			//me=!me;//每点击一次，轮到下家
			
		}
   }
		
        
		
		//统计赢法
		//遍历出所有赢的情况
		var wins=[];
		for(var i=0;i<15;i++)
		{
			wins[i]=[];
			for(var j=0;j<15;j++)
			{
				wins[i][j]=[];//三维数组
			}
		}
		//赢发数组
		//横线赢
		var count=0;//赢法索引
		for(var i=0;i<15;i++)
		{
			for(var j=0;j<11;j++)
			{
				for(k=0;k<5;k++)
				{
                    wins[i][j + k][count] = true;

                }
                count++;
			}
			
        }
    //竖线赢法
        for (var i = 0; i < 15; i++) {
            for (var j = 0; j < 11; j++) {
                for (k = 0; k < 5; k++) {
                    wins[j + k][i][count] = true;

                }
                count++;
            }

        }
		
    //斜线赢法
        for (var i = 0; i < 11; i++) {
            for (var j = 0; j < 11; j++) {
                for (k = 0; k < 5; k++) {
                    wins[i + k][j + k][count] = true;

                }
                count++;
            }

        }
		
        //反斜线
        for (var i = 0; i < 11; i++) {
            for (var j = 14; j > 3; j--) {
                for (k = 0; k < 5; k++) {
                    wins[i + k][j - k][count] = true;

                }
                count++;
            }
        }
        console.log(count);//572种
     var myWin = [];
     var computerWin = [];
     for (var i = 0; i < count; i++)
     {
         myWin[i] = 0;
         computerWin[i] = 0;
     }
	 
	 
	 
    //计算机ai算法
     var computerAi=function()
    {
         //alert("计算机下！")
         var mySource = [];//我方分数

         var computerSource = [];//计算机分数

         var max = 0;//保存最高点的分数
         var u = 0, v = 0;//最高点分数的坐标

         for (var i = 0; i < 15; i++)
         {
             mySource[i] = [];
             computerSource[i] = [];
             //初始化分数
             for (var j = 0; j < 15; j++)
             {
                 mySource[i][j] = 0;
                 computerSource[i][j] = 0;
             }
         }
         for (var i = 0; i < 15; i++)
         {
             for (var j = 0; j < 15; j++)
             {
                 if (chessborad[i][j] == 0)
                 {
                     for (var k = 0; k < count; k++)
                     {
                        
                         if (wins[i][j][k])
                         {
                              //我方下棋
                             if (myWin[k] == 1)
                             {
                                 mySource[i][j] += 200;//
                             }
                             else if (myWin[k] == 2)
                             {
                                 mySource[i][j] += 400;
                             }
                             else if (myWin[k] == 3) {
                                 mySource[i][j] += 2000;
                             }
                             else if (myWin[k] == 4) {
                                 mySource[i][j] += 10000;
                             }
                             //计算机下
                             if (computerWin[k] == 1)
                             {
                                 computerSource[i][j] += 200;//
                             }
                             else if (computerWin[k] == 2)
                             {
                                 computerSource[i][j] += 400;
                             }
                             else if (computerWin[k] == 3)
                             {
                                 computerSource[i][j] += 2000;
                             }
                             else if (computerWin[k] == 4)
                             {
                                 computerSource[i][j] += 10000;
                             }                                              
                         }
                     }
                     //我方
                     if (mySource[i][j] > max)
                     {
                         max = mySource[i][j];
                         u = i;
                         v = j;
                     }
                     else if (mySource[i][j] == max)
                     {
                         if (computerSource[i][j] > computerSource[u][v])
                         {
                             u = i;
                             v = j;
                         }
                     }


                     //电脑端
                     if (computerSource[i][j] > max)
                     {
                         max = computerSource[i][j];
                         u = i;
                         v = j;
                     }
                     else if (computerSource[i][j] == max)
                     {
                         if (mySource[i][j] > mySource[u][v])
                         {
                             u = i;
                             v = j;
                         }
                     }
                 }
             }
         }
         onStep(u, v, false);
         chessborad[u][v] = 2;
         for (var k = 0; k < count; k++)
         {
             if (wins[u][v][k])
             {
                 computerWin[k]++;
                 myWin[k] = 6;
                 if (computerWin[k] == 5)
                 {
                     alert("计算机赢了")
                     over = true;
					 //window.location.reload();
                 }
             }
         }
         if (!over)
         {
             me = !me;
         }

     }
	 window.onload=function()
    {
        
        var btu1 = document.getElementById("but1");
        var btu2 = document.getElementById("but2");
        var btu3 = document.getElementById("but3");

        btu1.onclick = function ()
        {
			
            window.location.reload();
        }
		btu2.onclick=function()
		{
			alert("不存在的！");
		}
        btu3.onclick = function ()
        {
            window.open('', '_self');
            window.close();
        }
	
	};

