#!/usr/bin/python3

from flask import Flask, jsonify, json, request, render_template
import clifford as cf
from clifford.g3c import *
from clifford.tools.g3c import *
import numpy as np
import math

ninf = einf
no = -eo

I3 = e123
I5 = e12345

app = Flask(__name__)


def as_3D_list(mv_3d):
    return  [mv_3d[1],mv_3d[2],mv_3d[3]]


@app.route("/")
def render_main():
    script = '''DrawSphere(-(3.0^e1234) - (2.0^e1235) + (2.0^e1245) - (1.0^e1345) + (1.0^e2345),rgb(255,0,0));
DrawPlane((0.57735^e1234) + (0.57735^e1235) - (0.57735^e1245) + (0.57735^e1345) - (0.57735^e2345),rgb(255,255,0));
DrawLine(-(0.70711^e124) - (0.70711^e125) - (0.70711^e145) - (0.70711^e245),rgb(255,0,255));
DrawCircle(-(0.07071^e124) + (0.07071^e125) - (0.07071^e134) + (0.07071^e135) + (0.70711^e145) + (0.07071^e234) - (0.07071^e235) - (0.70711^e245),rgb(0,0,255));
DrawPointPair((12.0^e12) - (16.0^e23) + (56.0^e24) + (60.0^e25),rgb(255,0,255));
DrawEucPoint(0.5^e1 + 0.5^e2 - 0.5^e3,rgb(255,0,0));'''
    return render_template('main.html', script=script)


@app.route("/demo/interpolate_circles")
def render_demo():
    script = '''DrawCircle((0.35652^e123) - (2.33275^e124) - (2.28623^e125) - (0.15416^e134) - (0.09628^e135) - (0.35866^e145) - (5.01848^e234) - (5.02537^e235) + (0.69989^e245) + (0.81784^e345),rgb(0, 255, 0));
DrawCircle((0.49663^e123) - (2.26814^e124) - (2.21184^e125) + (0.74584^e134) + (0.81888^e135) - (0.41811^e145) - (4.93936^e234) - (4.96672^e235) + (0.68492^e245) + (0.68529^e345),rgb(5, 249, 0));
DrawCircle((0.5746^e123) - (2.04695^e124) - (1.99092^e125) + (1.4626^e134) + (1.54543^e135) - (0.43771^e145) - (4.5081^e234) - (4.55881^e235) + (0.62021^e245) + (0.52083^e345),rgb(10, 244, 0));
DrawCircle((0.58843^e123) - (1.77914^e124) - (1.73071^e125) + (1.85892^e134) + (1.94833^e135) - (0.42336^e145) - (3.95383^e234) - (4.02445^e235) + (0.53896^e245) + (0.37772^e345),rgb(15, 239, 0));
DrawCircle((0.56617^e123) - (1.53934^e124) - (1.50134^e125) + (2.01457^e134) + (2.10959^e135) - (0.39357^e145) - (3.44368^e234) - (3.52961^e235) + (0.46476^e245) + (0.27222^e345),rgb(20, 234, 0));
DrawCircle((0.52986^e123) - (1.3453^e124) - (1.31806^e125) + (2.03815^e134) + (2.13876^e135) - (0.36023^e145) - (3.02359^e234) - (3.12141^e235) + (0.40379^e245) + (0.19787^e345),rgb(26, 228, 0));
DrawCircle((0.49022^e123) - (1.19175^e124) - (1.17469^e125) + (1.99805^e134) + (2.10447^e135) - (0.3282^e145) - (2.68679^e234) - (2.79433^e235) + (0.35488^e245) + (0.14494^e345),rgb(31, 223, 0));
DrawCircle((0.45157^e123) - (1.06934^e124) - (1.06171^e125) + (1.92957^e134) + (2.04202^e135) - (0.29892^e145) - (2.4155^e234) - (2.53143^e235) + (0.31537^e245) + (0.10616^e345),rgb(36, 218, 0));
DrawCircle((0.41534^e123) - (0.97012^e124) - (0.97117^e125) + (1.84995^e134) + (1.96863^e135) - (0.27254^e145) - (2.19364^e234) - (2.31714^e235) + (0.28293^e245) + (0.07675^e345),rgb(41, 213, 0));
DrawCircle((0.38185^e123) - (0.88818^e124) - (0.89729^e125) + (1.76748^e134) + (1.89255^e135) - (0.24878^e145) - (2.009^e234) - (2.13955^e235) + (0.25578^e245) + (0.05372^e345),rgb(46, 208, 0));
DrawCircle((0.35097^e123) - (0.81929^e124) - (0.83593^e125) + (1.68608^e134) + (1.81768^e135) - (0.22726^e145) - (1.85266^e234) - (1.98995^e235) + (0.23265^e245) + (0.03512^e345),rgb(52, 202, 0));
DrawCircle((0.32243^e123) - (0.76042^e124) - (0.78417^e125) + (1.60754^e134) + (1.7458^e135) - (0.20763^e145) - (1.7182^e234) - (1.86203^e235) + (0.21261^e245) + (0.01969^e345),rgb(57, 197, 0));
DrawCircle((0.29593^e123) - (0.70937^e124) - (0.73991^e125) + (1.53255^e134) + (1.6776^e135) - (0.18958^e145) - (1.60093^e234) - (1.75118^e235) + (0.195^e245) + (0.00656^e345),rgb(62, 192, 0));
DrawCircle((0.27119^e123) - (0.66455^e124) - (0.70159^e125) + (1.46128^e134) + (1.61326^e135) - (0.17284^e145) - (1.49736^e234) - (1.65399^e235) + (0.17931^e245) - (0.00484^e345),rgb(67, 187, 0));
DrawCircle((0.24796^e123) - (0.62474^e124) - (0.66808^e125) + (1.39363^e134) + (1.55269^e135) - (0.1572^e145) - (1.40487^e234) - (1.56788^e235) + (0.16517^e245) - (0.01495^e345),rgb(72, 182, 0));
DrawCircle((0.22602^e123) - (0.58903^e124) - (0.6385^e125) + (1.32938^e134) + (1.49569^e135) - (0.14247^e145) - (1.32147^e234) - (1.49088^e235) + (0.15229^e245) - (0.02408^e345),rgb(78, 176, 0));
DrawCircle((0.20518^e123) - (0.55671^e124) - (0.61218^e125) + (1.26826^e134) + (1.442^e135) - (0.12851^e145) - (1.24559^e234) - (1.42147^e235) + (0.14046^e245) - (0.03245^e345),rgb(83, 171, 0));
DrawCircle((0.18528^e123) - (0.52722^e124) - (0.58861^e125) + (1.20998^e134) + (1.39135^e135) - (0.11519^e145) - (1.17601^e234) - (1.35845^e235) + (0.12948^e245) - (0.04023^e345),rgb(88, 166, 0));
DrawCircle((0.16617^e123) - (0.50013^e124) - (0.56737^e125) + (1.15426^e134) + (1.34348^e135) - (0.10239^e145) - (1.11175^e234) - (1.30085^e235) + (0.11923^e245) - (0.04758^e345),rgb(93, 161, 0));
DrawCircle((0.14775^e123) - (0.47506^e124) - (0.54814^e125) + (1.10082^e134) + (1.29815^e135) - (0.09002^e145) - (1.052^e234) - (1.24791^e235) + (0.10958^e245) - (0.05459^e345),rgb(98, 156, 0));
DrawCircle((0.12988^e123) - (0.45174^e124) - (0.53064^e125) + (1.04942^e134) + (1.25515^e135) - (0.07799^e145) - (0.99612^e234) - (1.19899^e235) + (0.10045^e245) - (0.06137^e345),rgb(104, 150, 0));
DrawCircle((0.11249^e123) - (0.42992^e124) - (0.51467^e125) + (0.99983^e134) + (1.21426^e135) - (0.06624^e145) - (0.94356^e234) - (1.15357^e235) + (0.09174^e245) - (0.06797^e345),rgb(109, 145, 0));
DrawCircle((0.09548^e123) - (0.40939^e124) - (0.50003^e125) + (0.95181^e134) + (1.1753^e135) - (0.05469^e145) - (0.89387^e234) - (1.11122^e235) + (0.08339^e245) - (0.07448^e345),rgb(114, 140, 0));
DrawCircle((0.07876^e123) - (0.39^e124) - (0.48659^e125) + (0.90518^e134) + (1.13812^e135) - (0.04327^e145) - (0.84665^e234) - (1.07158^e235) + (0.07535^e245) - (0.08095^e345),rgb(119, 135, 0));
DrawCircle((0.06228^e123) - (0.37158^e124) - (0.47423^e125) + (0.85973^e134) + (1.10257^e135) - (0.03193^e145) - (0.80158^e234) - (1.03433^e235) + (0.06756^e245) - (0.08744^e345),rgb(124, 130, 0));
DrawCircle((0.04595^e123) - (0.35403^e124) - (0.46283^e125) + (0.81529^e134) + (1.06852^e135) - (0.02059^e145) - (0.75837^e234) - (0.99922^e235) + (0.05997^e245) - (0.094^e345),rgb(130, 124, 0));
DrawCircle((0.0297^e123) - (0.33722^e124) - (0.45232^e125) + (0.77167^e134) + (1.03587^e135) - (0.00921^e145) - (0.71676^e234) - (0.96603^e235) + (0.05255^e245) - (0.10068^e345),rgb(135, 119, 0));
DrawCircle((0.01348^e123) - (0.32107^e124) - (0.44263^e125) + (0.7287^e134) + (1.0045^e135) + (0.00229^e145) - (0.67652^e234) - (0.93456^e235) + (0.04526^e245) - (0.10754^e345),rgb(140, 114, 0));
DrawCircle(-(0.00279^e123) - (0.30549^e124) - (0.4337^e125) + (0.68622^e134) + (0.97434^e135) + (0.01397^e145) - (0.63746^e234) - (0.90464^e235) + (0.03805^e245) - (0.11463^e345),rgb(145, 109, 0));
DrawCircle(-(0.01917^e123) - (0.2904^e124) - (0.42547^e125) + (0.64404^e134) + (0.94531^e135) + (0.02591^e145) - (0.59938^e234) - (0.87612^e235) + (0.03091^e245) - (0.12202^e345),rgb(150, 104, 0));
DrawCircle(-(0.03573^e123) - (0.27573^e124) - (0.41792^e125) + (0.60199^e134) + (0.91736^e135) + (0.03819^e145) - (0.56211^e234) - (0.84888^e235) + (0.02378^e245) - (0.12977^e345),rgb(156, 98, 0));
DrawCircle(-(0.05253^e123) - (0.26142^e124) - (0.411^e125) + (0.55987^e134) + (0.89043^e135) + (0.0509^e145) - (0.52549^e234) - (0.8228^e235) + (0.01665^e245) - (0.13797^e345),rgb(161, 93, 0));
DrawCircle(-(0.06966^e123) - (0.2474^e124) - (0.40469^e125) + (0.51746^e134) + (0.86449^e135) + (0.06415^e145) - (0.48935^e234) - (0.79778^e235) + (0.00948^e245) - (0.14671^e345),rgb(166, 88, 0));
DrawCircle(-(0.08719^e123) - (0.23362^e124) - (0.39897^e125) + (0.47454^e134) + (0.83953^e135) + (0.07807^e145) - (0.45355^e234) - (0.77371^e235) + (0.00224^e245) - (0.15611^e345),rgb(171, 83, 0));
DrawCircle(-(0.1052^e123) - (0.22002^e124) - (0.39383^e125) + (0.43083^e134) + (0.81553^e135) + (0.09281^e145) - (0.41793^e234) - (0.75052^e235) - (0.00511^e245) - (0.16629^e345),rgb(176, 78, 0));
DrawCircle(-(0.12378^e123) - (0.20654^e124) - (0.38925^e125) + (0.386^e134) + (0.79252^e135) + (0.10857^e145) - (0.38234^e234) - (0.7281^e235) - (0.0126^e245) - (0.17743^e345),rgb(182, 72, 0));
DrawCircle(-(0.14302^e123) - (0.19313^e124) - (0.38521^e125) + (0.33969^e134) + (0.77056^e135) + (0.12558^e145) - (0.34661^e234) - (0.70636^e235) - (0.02026^e245) - (0.18974^e345),rgb(187, 67, 0));
DrawCircle(-(0.16301^e123) - (0.17971^e124) - (0.3817^e125) + (0.29142^e134) + (0.74971^e135) + (0.14414^e145) - (0.31059^e234) - (0.68521^e235) - (0.02813^e245) - (0.2035^e345),rgb(192, 62, 0));
DrawCircle(-(0.18382^e123) - (0.16623^e124) - (0.37867^e125) + (0.24058^e134) + (0.73012^e135) + (0.16466^e145) - (0.27411^e234) - (0.66449^e235) - (0.03624^e245) - (0.21906^e345),rgb(197, 57, 0));
DrawCircle(-(0.2055^e123) - (0.15262^e124) - (0.37605^e125) + (0.18641^e134) + (0.71199^e135) + (0.18764^e145) - (0.237^e234) - (0.64403^e235) - (0.0446^e245) - (0.23691^e345),rgb(202, 52, 0));
DrawCircle(-(0.22803^e123) - (0.1388^e124) - (0.3737^e125) + (0.1279^e134) + (0.69561^e135) + (0.21381^e145) - (0.19912^e234) - (0.62354^e235) - (0.05321^e245) - (0.2577^e345),rgb(208, 46, 0));
DrawCircle(-(0.25121^e123) - (0.12469^e124) - (0.37132^e125) + (0.06367^e134) + (0.68142^e135) + (0.24412^e145) - (0.16038^e234) - (0.60255^e235) - (0.06202^e245) - (0.28232^e345),rgb(213, 41, 0));
DrawCircle(-(0.27454^e123) - (0.11021^e124) - (0.36838^e125) - (0.00814^e134) + (0.67008^e135) + (0.27992^e145) - (0.1208^e234) - (0.58027^e235) - (0.07085^e245) - (0.31205^e345),rgb(218, 36, 0));
DrawCircle(-(0.29681^e123) - (0.09528^e124) - (0.36377^e125) - (0.09007^e134) + (0.66252^e135) + (0.32308^e145) - (0.0807^e234) - (0.55525^e235) - (0.07933^e245) - (0.34865^e345),rgb(223, 31, 0));
DrawCircle(-(0.31532^e123) - (0.07986^e124) - (0.35529^e125) - (0.18542^e134) + (0.66007^e135) + (0.37609^e145) - (0.04108^e234) - (0.52473^e235) - (0.08661^e245) - (0.39454^e345),rgb(228, 26, 0));
DrawCircle(-(0.32431^e123) - (0.06399^e124) - (0.33847^e125) - (0.29777^e134) + (0.66436^e135) + (0.44186^e145) - (0.00432^e234) - (0.48336^e235) - (0.09086^e245) - (0.45264^e345),rgb(234, 20, 0));
DrawCircle(-(0.3121^e123) - (0.04789^e124) - (0.30467^e125) - (0.42831^e134) + (0.6766^e135) + (0.52193^e145) + (0.02447^e234) - (0.42114^e235) - (0.0885^e245) - (0.5249^e345),rgb(239, 15, 0));
DrawCircle(-(0.25917^e123) - (0.03196^e124) - (0.23993^e125) - (0.56688^e134) + (0.69488^e135) + (0.61049^e145) + (0.03664^e234) - (0.3224^e235) - (0.07367^e245) - (0.60695^e345),rgb(244, 10, 0));
DrawCircle(-(0.14875^e123) - (0.01632^e124) - (0.13315^e125) - (0.67696^e134) + (0.70956^e135) + (0.68379^e145) + (0.02526^e234) - (0.1755^e235) - (0.04186^e245) - (0.67822^e345),rgb(249, 5, 0));
DrawCircle(-(0.70711^e134) + (0.70711^e135) + (0.70711^e145) - (0.70711^e345),rgb(255, 0, 0));'''
    return render_template('main.html', script=script)


@app.route("/demo/cluster_circles")
def render_demo():
    script = '''DrawCircle(-(0.83117^e123) - (3.63505^e124) - (3.75165^e125) - (0.45118^e134) - (0.46211^e135) + (0.0155^e145) + (1.80643^e234) + (1.96801^e235) + (0.45325^e245) + (0.06396^e345),rgb(0, 255, 0));
DrawCircle(-(0.87777^e123) - (4.07101^e124) - (4.20429^e125) + (0.03592^e134) + (0.04627^e135) + (0.04258^e145) + (1.41833^e234) + (1.56649^e235) + (0.47179^e245) + (0.01067^e345),rgb(0, 255, 0));
DrawCircle(-(0.95916^e123) - (4.36065^e124) - (4.47651^e125) - (0.604^e134) - (0.60334^e135) + (0.07592^e145) + (1.78727^e234) + (1.94974^e235) + (0.52273^e245) + (0.10352^e345),rgb(0, 255, 0));
DrawCircle(-(0.99584^e123) - (4.46004^e124) - (4.57868^e125) - (0.68855^e134) - (0.7022^e135) + (0.02089^e145) + (1.9987^e234) + (2.15857^e235) + (0.47793^e245) + (0.08314^e345),rgb(0, 255, 0));
DrawCircle(-(0.96921^e123) - (4.51716^e124) - (4.64409^e125) - (0.18274^e134) - (0.19153^e135) - (0.01703^e145) + (1.60117^e234) + (1.7549^e235) + (0.50677^e245) + (0.01446^e345),rgb(0, 255, 0));
DrawCircle(-(0.91513^e123) - (4.12658^e124) - (4.23566^e125) + (0.03299^e134) + (0.04334^e135) + (0.04275^e145) + (1.82612^e234) + (1.9929^e235) + (0.53442^e245) + (0.01465^e345),rgb(0, 255, 0));
DrawCircle(-(0.90393^e123) - (4.18091^e124) - (4.313^e125) - (0.71041^e134) - (0.72361^e135) + (0.04276^e145) + (1.34005^e234) + (1.48904^e235) + (0.4933^e245) + (0.09753^e345),rgb(0, 255, 0));
DrawCircle(-(0.88819^e123) - (4.04275^e124) - (4.16082^e125) - (0.38731^e134) - (0.40619^e135) - (0.03445^e145) + (1.60771^e234) + (1.76747^e235) + (0.51346^e245) + (0.03549^e345),rgb(0, 255, 0));
DrawCircle(-(0.91004^e123) - (3.67265^e124) - (3.76736^e125) - (0.31066^e134) - (0.30199^e135) + (0.06732^e145) + (2.53409^e234) + (2.70952^e235) + (0.44428^e245) + (0.08403^e345),rgb(0, 255, 0));
DrawCircle(-(0.9603^e123) - (4.20464^e124) - (4.32252^e125) - (0.46237^e134) - (0.47105^e135) + (0.01877^e145) + (2.12335^e234) + (2.28414^e235) + (0.44335^e245) + (0.05823^e345),rgb(0, 255, 0));
DrawCircle((0.02168^e123) + (0.37713^e124) + (0.23388^e125) + (0.16284^e134) + (0.04091^e135) - (1.04502^e145) - (0.04037^e234) - (0.01702^e235) + (0.13941^e245) - (0.05167^e345),rgb(255, 0, 0));
DrawCircle((0.05628^e123) + (0.5128^e124) + (0.37734^e125) + (0.03539^e134) - (0.08565^e135) - (1.01764^e145) - (0.11869^e234) - (0.06457^e235) + (0.2075^e245) - (0.22123^e345),rgb(255, 0, 0));
DrawCircle((0.05847^e123) + (0.64889^e124) + (0.50296^e125) + (0.06663^e134) - (0.03996^e135) - (1.01663^e145) - (0.10854^e234) - (0.05135^e235) + (0.36382^e245) - (0.13269^e345),rgb(255, 0, 0));
DrawCircle((0.04651^e123) + (0.58388^e124) + (0.44733^e125) + (0.17334^e134) + (0.04911^e135) - (1.05056^e145) - (0.09858^e234) - (0.05553^e235) + (0.25097^e245) - (0.10286^e345),rgb(255, 0, 0));
DrawCircle((0.06111^e123) + (0.54627^e124) + (0.40098^e125) + (0.00395^e134) - (0.11481^e135) - (1.05222^e145) - (0.07461^e234) - (0.0479^e235) + (0.06141^e245) - (0.14327^e345),rgb(255, 0, 0));
DrawCircle((0.03344^e123) + (0.45933^e124) + (0.33256^e125) + (0.18767^e134) + (0.06267^e135) - (1.00567^e145) - (0.15793^e234) - (0.09287^e235) + (0.29497^e245) - (0.22526^e345),rgb(255, 0, 0));
DrawCircle((0.04643^e123) + (0.69773^e124) + (0.56454^e125) + (0.28537^e134) + (0.15943^e135) - (1.07391^e145) - (0.16483^e234) - (0.11653^e235) + (0.25304^e245) - (0.15021^e345),rgb(255, 0, 0));
DrawCircle((0.02881^e123) + (0.48609^e124) + (0.33809^e125) + (0.1492^e134) + (0.0425^e135) - (1.0338^e145) - (0.13194^e234) - (0.08053^e235) + (0.18968^e245) - (0.22239^e345),rgb(255, 0, 0));
DrawCircle((0.06883^e123) + (0.59873^e124) + (0.46428^e125) + (0.02262^e134) - (0.10126^e135) - (1.03347^e145) - (0.12803^e234) - (0.07797^e235) + (0.18541^e245) - (0.21399^e345),rgb(255, 0, 0));
DrawCircle((0.0046^e123) + (0.21734^e124) + (0.0862^e125) + (0.16851^e134) + (0.04611^e135) - (0.98017^e145) - (0.09269^e234) - (0.03145^e235) + (0.25137^e245) - (0.22314^e345),rgb(255, 0, 0));
DrawCircle((0.07258^e123) + (0.46323^e124) + (0.23531^e125) - (0.01121^e134) + (0.03494^e135) + (0.25936^e145) + (0.21171^e234) + (0.26798^e235) + (1.024^e245) - (0.14331^e345),rgb(127, 127, 0));
DrawCircle((0.15159^e123) + (0.67567^e124) + (0.44544^e125) + (0.09615^e134) + (0.13393^e135) + (0.31443^e145) + (0.53619^e234) + (0.58921^e235) + (1.05065^e245) - (0.10002^e345),rgb(127, 127, 0));
DrawCircle((0.01461^e123) + (1.0876^e124) + (0.85754^e125) - (0.19874^e134) - (0.15226^e135) + (0.33083^e145) - (0.14596^e234) - (0.09955^e235) + (1.15676^e245) - (0.16698^e345),rgb(127, 127, 0));
DrawCircle((0.03334^e123) + (0.8514^e124) + (0.62062^e125) - (0.09851^e134) - (0.05606^e135) + (0.40205^e145) - (0.01591^e234) + (0.03078^e235) + (1.08222^e245) - (0.1177^e345),rgb(127, 127, 0));
DrawCircle((0.02389^e123) + (0.835^e124) + (0.60289^e125) - (0.07057^e134) - (0.03888^e135) + (0.42173^e145) - (0.06394^e234) - (0.01535^e235) + (1.07719^e245) - (0.05874^e345),rgb(127, 127, 0));
DrawCircle((0.05911^e123) + (0.76288^e124) + (0.53659^e125) - (0.04923^e134) - (0.009^e135) + (0.33076^e145) + (0.05846^e234) + (0.1249^e235) + (1.08133^e245) - (0.09513^e345),rgb(127, 127, 0));
DrawCircle(-(0.00014^e123) + (0.69145^e124) + (0.46445^e125) - (0.17387^e134) - (0.11689^e135) + (0.47293^e145) - (0.15195^e234) - (0.10228^e235) + (1.02201^e245) - (0.15306^e345),rgb(127, 127, 0));
DrawCircle((0.07478^e123) + (0.6203^e124) + (0.38878^e125) - (0.02035^e134) + (0.03072^e135) + (0.36063^e145) + (0.24651^e234) + (0.27864^e235) + (1.02975^e245) - (0.1771^e345),rgb(127, 127, 0));
DrawCircle((0.08187^e123) + (0.59312^e124) + (0.36135^e125) + (0.07161^e134) + (0.10145^e135) + (0.41895^e145) + (0.22544^e234) + (0.27675^e235) + (1.00999^e245) - (0.0373^e345),rgb(127, 127, 0));
DrawCircle((0.05451^e123) + (0.66172^e124) + (0.43241^e125) - (0.05398^e134) + (0.00843^e135) + (0.53049^e145) + (0.14921^e234) + (0.17682^e235) + (0.96282^e245) - (0.19816^e345),rgb(127, 127, 0));
DrawCircle(-(0.92579^e123) - (4.15641^e124) - (4.27513^e125) - (0.37489^e134) - (0.3794^e135) + (0.02786^e145) + (1.8071^e234) + (1.96808^e235) + (0.49097^e245) + (0.0564^e345),rgb(0,0,0));
DrawCircle((0.05566^e123) + (0.72782^e124) + (0.4971^e125) - (0.04809^e134) - (0.00334^e135) + (0.3857^e145) + (0.10376^e234) + (0.1515^e235) + (1.05429^e245) - (0.12464^e345),rgb(0,0,0));
DrawCircle((0.0429^e123) + (0.51529^e124) + (0.37667^e125) + (0.12629^e134) + (0.00609^e135) - (1.03559^e145) - (0.11115^e234) - (0.06288^e235) + (0.22063^e245) - (0.1693^e345),rgb(0,0,0));'''
    return render_template('main.html', script=script)


@app.route("/to_point_pair/",methods=['POST'])
def to_point_pair():
    print('RECIEVING POINT PAIR')
    present_blades_dict = json.loads(request.form.get('present_blades'))
    print('Recieved blade values: ',present_blades_dict)
    point_pair = layout.dict_to_multivector(present_blades_dict)
    print('Point pair: ',point_pair)
    A,B = point_pair_to_end_points(point_pair)
    a = as_3D_list(down(A))
    b = as_3D_list(down(B))
    print('a: ',a)
    print('b: ',b)
    return jsonify(a=a,b=b)


@app.route("/to_sphere/",methods=['POST'])
def to_sphere():
    print('RECIEVING SPHERE')
    present_blades_dict = json.loads(request.form.get('present_blades'))
    print('Recieved blade values: ',present_blades_dict)
    sphere = layout.dict_to_multivector(present_blades_dict)
    print('Sphere: ',sphere)
    GAcentre = down(get_center_from_sphere(sphere))
    centre = as_3D_list(GAcentre)
    radius = get_radius_from_sphere(sphere)
    print('Centre: ',centre)
    print('Radius: ',radius)
    return jsonify(centre=centre,radius=radius)


@app.route("/to_plane/",methods=['POST'])
def to_plane():
    print('RECIEVING PLANE')
    present_blades_dict = json.loads(request.form.get('present_blades'))
    print('Recieved blade values: ',present_blades_dict)
    plane = layout.dict_to_multivector(present_blades_dict)
    print('Plane: ',plane)
    normalGA = get_plane_normal(plane)
    normal = as_3D_list(normalGA)
    distance = get_plane_origin_distance(plane)
    print('Distance: ', distance)
    print('Normal: ', normal)
    return jsonify(distance=distance,normal=normal) 


@app.route("/to_line/",methods=['POST'])
def to_line():
    print('RECIEVING LINE')
    present_blades_dict = json.loads(request.form.get('present_blades'))
    print('Recieved blade values: ',present_blades_dict)
    line = layout.dict_to_multivector(present_blades_dict)
    print('Line: ',line)
    GApoint,GAdirection = line_to_point_and_direction(line)
    point = as_3D_list(GApoint)
    direction = as_3D_list(GAdirection)
    print('Point: ', point)
    print('Direction: ', direction)
    return jsonify(point=point,direction=direction) 


@app.route("/to_circle/",methods=['POST'])
def to_circle():
    print('RECIEVING CIRCLE')
    present_blades_dict = json.loads(request.form.get('present_blades'))
    print('Recieved blade values: ',present_blades_dict)
    circle = layout.dict_to_multivector(present_blades_dict)
    print('Circle: ',circle)

    GAcentre,GAnormal,radius = get_circle_in_euc(circle);

    centre = as_3D_list(GAcentre)
    normal = as_3D_list(GAnormal)
    print('Radius: ', radius)
    print('Centre: ', centre)
    print('Normal: ', normal)
    return jsonify(centre=centre,normal=normal,radius=radius) 


if __name__ == '__main__':
  app.run()
