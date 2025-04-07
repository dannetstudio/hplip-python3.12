/*****************************************************************************\
  dj660_maps.cpp : Color maps for the DJ660

  Copyright (c) 1996 - 2015, HP Co.
  All rights reserved.

  Redistribution and use in source and binary forms, with or without
  modification, are permitted provided that the following conditions
  are met:
  1. Redistributions of source code must retain the above copyright
     notice, this list of conditions and the following disclaimer.
  2. Redistributions in binary form must reproduce the above copyright
     notice, this list of conditions and the following disclaimer in the
     documentation and/or other materials provided with the distribution.
  3. Neither the name of HP nor the names of its
     contributors may be used to endorse or promote products derived
     from this software without specific prior written permission.

  THIS SOFTWARE IS PROVIDED BY THE AUTHOR "AS IS" AND ANY EXPRESS OR IMPLIED
  WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
  MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.  IN
  NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
  TO, PATENT INFRINGEMENT; PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
  OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
  ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
  THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
\*****************************************************************************/


#include "config.h"

#include "global_types.h"

APDK_BEGIN_NAMESPACE

//const
uint32_t ulMapDJ660_CCM_KCMY[ 9 * 9 * 9 ]=
    {
        422720226UL, 142187374UL, 94354238UL, 62442785UL, 45668877UL, 27648516UL, 8972032UL, 7335680UL, 5895424UL,
2519110233UL, 807846483UL, 391693109UL, 260029471UL, 143570703UL, 42776580UL, 8501760UL, 7782400UL, 6539520UL,
3072173868UL, 1881129514UL, 841465387UL, 524792087UL, 358391818UL, 174364420UL, 40408577UL, 6920704UL, 6530560UL,
3407591425UL, 2551891200UL, 1612695808UL, 824489479UL, 506699268UL, 306153730UL, 105283329UL, 5144320UL, 5737216UL,
3289364224UL, 2584592128UL, 1829749504UL, 1142143232UL, 639280640UL, 405048832UL, 204241920UL, 53835264UL, 4290816UL,
2970005760UL, 2449717248UL, 1862580992UL, 1325905408UL, 856467712UL, 487757568UL, 270041856UL, 119436800UL, 2650624UL,
2583865856UL, 2214636288UL, 1811983360UL, 1392618240UL, 973382656UL, 621320448UL, 336235520UL, 152010496UL, 1405952UL,
2197856768UL, 1996530176UL, 1711316992UL, 1375772160UL, 1040226048UL, 721654784UL, 436506368UL, 184846592UL, 622592UL,
1879088896UL, 1778424576UL, 1593874176UL, 1342214912UL, 1073778688UL, 788565504UL, 536907264UL, 268472320UL, 37120UL,
2191458944UL, 130097257UL, 63659581UL, 30835745UL, 30318351UL, 28684549UL, 9946880UL, 8574976UL, 7855360UL,
2351640941UL, 1230197602UL, 763002927UL, 394890269UL, 193893645UL, 59415555UL, 8365312UL, 7515392UL, 6534656UL,
2938266166UL, 2184740132UL, 1212123679UL, 760318735UL, 459048710UL, 173835267UL, 22906624UL, 6065408UL, 5544192UL,
3273752070UL, 2552530688UL, 1730711808UL, 1043106817UL, 641040129UL, 373061120UL, 104886784UL, 4355584UL, 4489984UL,
3155526144UL, 2501084160UL, 1846774528UL, 1242990592UL, 807173632UL, 488796928UL, 220555776UL, 53111296UL, 3305728UL,
2970190592UL, 2399567872UL, 1829078016UL, 1342538496UL, 940211456UL, 588280832UL, 286354176UL, 102065408UL, 1992448UL,
2802024960UL, 2231400192UL, 1795192832UL, 1375762944UL, 1023440896UL, 721712640UL, 436629248UL, 168257792UL, 813056UL,
2583724288UL, 2097182464UL, 1744860672UL, 1409316864UL, 1124104448UL, 822113792UL, 520122624UL, 251686400UL, 225024UL,
2315289088UL, 1996520960UL, 1694530816UL, 1392540928UL, 1124105216UL, 872446720UL, 620787968UL, 352352768UL, 31744UL,
2813265494UL, 886309456UL, 47912514UL, 31343650UL, 47801870UL, 30114052UL, 11901184UL, 10791936UL, 9878016UL,
2858360649UL, 1938110261UL, 764624176UL, 429676569UL, 211511561UL, 43283459UL, 9142784UL, 8359936UL, 7380736UL,
2788045111UL, 2135115815UL, 1701143808UL, 1080584704UL, 577202944UL, 224619520UL, 6057728UL, 5864704UL, 5343744UL,
3056161036UL, 2435668741UL, 1815635456UL, 1195009792UL, 725443840UL, 373187328UL, 104752128UL, 3894016UL, 3831552UL,
2988071680UL, 2400804096UL, 1847354112UL, 1293771776UL, 857694464UL, 488791552UL, 220486400UL, 52715264UL, 2582272UL,
2920177152UL, 2332777728UL, 1829330688UL, 1359503616UL, 973824256UL, 621763840UL, 269506560UL, 118642944UL, 1335040UL,
2886099200UL, 2265144064UL, 1778407680UL, 1392532480UL, 1073766144UL, 755195648UL, 453270272UL, 184834304UL, 482560UL,
2852218112UL, 2197838848UL, 1811963136UL, 1476419840UL, 1191208192UL, 889218048UL, 587227392UL, 302014208UL, 25088UL,
2717935872UL, 2231395840UL, 1811965440UL, 1476421888UL, 1191209984UL, 939551744UL, 687892736UL, 402679808UL, 27136UL,
3249604153UL, 1708524086UL, 585171507UL, 48370214UL, 31601680UL, 14372868UL, 13461760UL, 12680448UL, 11702272UL,
3195409712UL, 2224038185UL, 1083974180UL, 396241692UL, 178339850UL, 43994626UL, 10051072UL, 9596416UL, 8880128UL,
3007980834UL, 2337813271UL, 1785678080UL, 1081100800UL, 561007616UL, 191713280UL, 6706688UL, 6514176UL, 6124544UL,
2838245394UL, 2301901833UL, 1799440128UL, 1128481536UL, 742672896UL, 356862976UL, 105075200UL, 4217344UL, 4024320UL,
2871016960UL, 2300592640UL, 1797474304UL, 1311000576UL, 874990080UL, 505956608UL, 220744448UL, 52842752UL, 2382848UL,
2836546048UL, 2249147648UL, 1779386112UL, 1359956224UL, 974146048UL, 605243648UL, 320030720UL, 101862400UL, 1135360UL,
2903066112UL, 2214872320UL, 1778665216UL, 1426278656UL, 1090735104UL, 755256320UL, 436488960UL, 184830720UL, 282368UL,
3003337216UL, 2264942592UL, 1862290176UL, 1526747136UL, 1191203584UL, 889213696UL, 604000512UL, 318787840UL, 21248UL,
3070251008UL, 2432716800UL, 1929400832UL, 1577080320UL, 1258314496UL, 989879296UL, 738220800UL, 436230400UL, 22784UL,
3568109346UL, 2262106917UL, 1122173220UL, 367395105UL, 31854613UL, 15083526UL, 14368512UL, 13717760UL, 13067776UL,
3447722013UL, 2459112987UL, 1369380887UL, 547296537UL, 195174925UL, 44445699UL, 10698496UL, 10439936UL, 10182144UL,
3143179283UL, 2439259148UL, 1785868800UL, 1098199552UL, 561329152UL, 192231424UL, 7487232UL, 7621632UL, 7428352UL,
2856002824UL, 2302618117UL, 1766339072UL, 1212887808UL, 726479872UL, 340670208UL, 89013504UL, 5064192UL, 4871424UL,
2770675968UL, 2217095168UL, 1730819072UL, 1261188352UL, 842150400UL, 489698816UL, 204552704UL, 53363200UL, 2968832UL,
2752916736UL, 2165649920UL, 1712731648UL, 1310078464UL, 957822464UL, 605632256UL, 303642624UL, 102251776UL, 1394176UL,
2886480128UL, 2198352896UL, 1728526080UL, 1376139264UL, 1040595200UL, 721893888UL, 436746752UL, 185023232UL, 475392UL,
3104126208UL, 2298623744UL, 1828731392UL, 1476410624UL, 1157644288UL, 855654656UL, 570441728UL, 285229056UL, 17408UL,
3338680832UL, 2550152192UL, 1996505088UL, 1610630400UL, 1308641536UL, 1006652416UL, 754994176UL, 436226816UL, 18944UL,
3752199442UL, 2714829590UL, 1608712727UL, 786891031UL, 266863123UL, 15403531UL, 15080962UL, 14429952UL, 13975808UL,
3565226513UL, 2610105871UL, 1587482636UL, 832573198UL, 228527886UL, 44439813UL, 11020288UL, 11023360UL, 11091712UL,
3160347149UL, 2439583495UL, 1769086464UL, 1114971648UL, 527834880UL, 175710720UL, 8006144UL, 8336896UL, 8536320UL,
2789414919UL, 2235964420UL, 1749885184UL, 1213211136UL, 726868480UL, 324412160UL, 89664000UL, 5976832UL, 6111488UL,
2670533632UL, 2150506752UL, 1680941824UL, 1261642752UL, 859251456UL, 473506816UL, 188360704UL, 3747328UL, 3947264UL,
2702777344UL, 2082087680UL, 1629168896UL, 1260135936UL, 924722432UL, 572662272UL, 287385088UL, 86060032UL, 2176512UL,
2886606592UL, 2114724864UL, 1644898048UL, 1292577024UL, 990652416UL, 688727808UL, 386803968UL, 151857920UL, 930304UL,
3171230464UL, 2265130496UL, 1711286016UL, 1375742464UL, 1090530304UL, 839003904UL, 553857024UL, 268644352UL, 209664UL,
3540002560UL, 2583702016UL, 1962946304UL, 1610625792UL, 1308636928UL, 1023425024UL, 738212608UL, 436222720UL, 14848UL,
3819438857UL, 3083666187UL, 2028077070UL, 1189478414UL, 652804109UL, 250413065UL, 15598599UL, 15144192UL, 14820608UL,
3632465161UL, 2693924616UL, 1738344454UL, 1050674951UL, 530646791UL, 94635528UL, 27923458UL, 11411200UL, 11806464UL,
3143895559UL, 2439646467UL, 1735462912UL, 1131745024UL, 611847936UL, 209326336UL, 8198144UL, 8791040UL, 9382656UL,
2689011205UL, 2185891842UL, 1716523520UL, 1196626432UL, 743903488UL, 307827200UL, 73341184UL, 6627840UL, 7154944UL,
2587038208UL, 2067010560UL, 1647711488UL, 1228477952UL, 842863872UL, 440341504UL, 155326208UL, 4529664UL, 4926208UL,
2635993600UL, 2015368960UL, 1579161344UL, 1210259200UL, 874780160UL, 539497984UL, 254351104UL, 69934080UL, 3090176UL,
2869890816UL, 2081429504UL, 1578113536UL, 1242569216UL, 957422080UL, 655563008UL, 387389184UL, 135666432UL, 1581568UL,
3238466560UL, 2248480768UL, 1677990656UL, 1325669632UL, 1040457216UL, 772087296UL, 503717120UL, 235282176UL, 533248UL,
3724548096UL, 2617252608UL, 1895833344UL, 1526735616UL, 1241523712UL, 973088768UL, 704653312UL, 402663424UL, 10240UL,
3754033155UL, 3252158469UL, 2414215174UL, 1625948167UL, 1089339398UL, 653393924UL, 301334531UL, 15925254UL, 15732736UL,
3616342532UL, 2777940483UL, 1872626178UL, 1252262146UL, 765985026UL, 380240130UL, 44958469UL, 11668480UL, 12325888UL,
3144155907UL, 2439775233UL, 1718682624UL, 1165427712UL, 695993088UL, 310313984UL, 58918914UL, 9114112UL, 9770752UL,
2672559362UL, 2186151169UL, 1699939840UL, 1196885248UL, 760939776UL, 375391488UL, 90507776UL, 7082496UL, 7608320UL,
2486700288UL, 2017003520UL, 1614481664UL, 1212024832UL, 843122432UL, 474285824UL, 155781376UL, 5050112UL, 5641984UL,
2552498432UL, 1965361920UL, 1546062336UL, 1193806592UL, 858393088UL, 539822336UL, 254806528UL, 53808640UL, 3872000UL,
2819885312UL, 2064911360UL, 1561660672UL, 1192627200UL, 890702848UL, 605621248UL, 337316608UL, 119409920UL, 2298624UL,
3288794880UL, 2282097664UL, 1644563968UL, 1241911040UL, 939986944UL, 688393984UL, 436866560UL, 185273088UL, 921856UL,
3875539712UL, 2701135104UL, 1879052032UL, 1409290752UL, 1107301376UL, 855643392UL, 620762368UL, 335549440UL, 5376UL,
3539009536UL, 3170041856UL, 2666856448UL, 2096496640UL, 1559756800UL, 1090125824UL, 721158144UL, 352124928UL, 16711680UL,
3433627648UL, 2795896832UL, 2125332480UL, 1572143104UL, 1119551488UL, 750780416UL, 432275456UL, 180748288UL, 13041664UL,
3111387136UL, 2507407360UL, 1887109120UL, 1350828032UL, 931725312UL, 563019776UL, 278200320UL, 77070336UL, 10158080UL,
2689794048UL, 2253717504UL, 1784283136UL, 1314914304UL, 895811584UL, 527106048UL, 258998272UL, 58064896UL, 8126464UL,
2436694016UL, 2050949120UL, 1665204224UL, 1279524864UL, 910753792UL, 575537152UL, 273874944UL, 72941568UL, 6291456UL,
2469003264UL, 1948975104UL, 1579941888UL, 1227816960UL, 909115392UL, 607453184UL, 322568192UL, 104792064UL, 4653056UL,
2803433472UL, 2098790400UL, 1595539456UL, 1192951808UL, 874315776UL, 606011392UL, 371326976UL, 153550848UL, 3080192UL,
3339386880UL, 2416508928UL, 1711931392UL, 1242169344UL, 889978880UL, 621608960UL, 403636224UL, 185729024UL, 1507328UL,
4026531840UL, 2936012800UL, 2030043136UL, 1409286144UL, 1006632960UL, 704643072UL, 469762048UL, 234881024UL, 0
    };

APDK_END_NAMESPACE

