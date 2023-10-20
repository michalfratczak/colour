# !/usr/bin/env python
"""Define the unit tests for the :mod:`colour.colorimetry.blackbody` module."""

from __future__ import annotations

import unittest
from itertools import product

import numpy as np

from colour.colorimetry import (
    SpectralShape,
    planck_law,
    rayleigh_jeans_law,
    sd_blackbody,
    sd_rayleigh_jeans,
)
from colour.hints import NDArrayFloat
from colour.utilities import ignore_numpy_errors

__author__ = "Colour Developers"
__copyright__ = "Copyright 2013 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "DATA_PLANCK_LAW",
    "DATA_BLACKBODY",
    "DATA_RAYLEIGH_JEANS_LAW",
    "DATA_RAYLEIGH_JEANS",
    "TestPlanckLaw",
    "TestSdBlackbody",
    "TestRayleighJeansLaw",
    "TestSdRayleighJeans",
]


DATA_PLANCK_LAW: dict = {
    1667: np.array(
        [
            0.000000000000000e000,
            0.000000000000000e000,
            0.000000000000000e000,
            0.000000000000000e000,
            6.006134512060715e-212,
            2.581138199699265e-096,
            2.991192553728005e-039,
            1.800055676589435e-011,
            2.468492049044663e002,
            1.615956484003356e008,
            2.311790654845391e010,
            4.959729128263715e010,
            1.429819160471000e010,
            1.728272063092092e009,
            1.454720412629704e008,
            1.046192398426646e007,
        ]
    ),
    5000: np.array(
        [
            0.000000000000000e000,
            0.000000000000000e000,
            0.000000000000000e000,
            2.211832608569335e-132,
            8.860635033018581e-056,
            3.135062153702092e-018,
            3.296566337346393e000,
            5.975780855300837e008,
            1.422301922547989e012,
            1.231071705140845e013,
            6.775708530833963e012,
            1.074763978522569e012,
            1.013929733763001e011,
            7.670601003755050e009,
            5.254367965012848e008,
            3.434696144765859e007,
        ]
    ),
    10000: np.array(
        [
            0.000000000000000e000,
            0.000000000000000e000,
            7.077864347421871e-131,
            2.835403210565946e-054,
            1.003219889184669e-016,
            1.054901227950846e002,
            1.912249873696268e010,
            4.551366152153565e013,
            3.939429456450704e014,
            2.168226729866868e014,
            3.439244731272221e013,
            3.244575148041603e012,
            2.454592321201616e011,
            1.681397748804111e010,
            1.099102766325075e009,
            7.023565300892627e007,
        ]
    ),
    100000: np.array(
        [
            3.887203488469926e-34,
            2.126338122524389e-04,
            2.780064431399975e10,
            5.619415522222338e16,
            1.412499469182817e19,
            4.002679163635765e19,
            1.309621960617621e19,
            1.668675488105569e18,
            1.436224908464434e17,
            1.043271214642522e16,
            7.012275974522810e14,
            4.542159102349822e13,
            2.889595565075848e12,
            1.821997118722198e11,
            1.143770312696396e10,
            7.164293165970466e08,
        ]
    ),
    10000000000000000000: np.array(
        [
            8.278028225847591e40,
            5.173767641156605e39,
            3.233604775723460e38,
            2.021002984827344e37,
            1.263126865517147e36,
            7.894542909482346e34,
            4.934089318426522e33,
            3.083805824016593e32,
            1.927378640010376e31,
            1.204611650006487e30,
            7.528822812540548e28,
            4.705514257837843e27,
            2.940946411148653e26,
            1.838091506967908e25,
            1.148807191854943e24,
            7.180044949093393e22,
        ]
    ),
}

DATA_BLACKBODY: NDArrayFloat = np.array(
    [
        6654.27827064,
        6709.60527925,
        6764.82512152,
        6819.93307864,
        6874.92448983,
        6929.79475262,
        6984.53932320,
        7039.15371664,
        7093.63350719,
        7147.97432845,
        7202.17187363,
        7256.22189565,
        7310.12020737,
        7363.86268165,
        7417.44525154,
        7470.86391025,
        7524.11471135,
        7577.19376869,
        7630.09725652,
        7682.82140944,
        7735.36252240,
        7787.71695067,
        7839.88110979,
        7891.85147549,
        7943.62458362,
        7995.19703005,
        8046.56547051,
        8097.72662050,
        8148.67725513,
        8199.41420894,
        8249.93437573,
        8300.23470836,
        8350.31221854,
        8400.16397663,
        8449.78711137,
        8499.17880967,
        8548.33631631,
        8597.25693372,
        8645.93802164,
        8694.37699689,
        8742.57133299,
        8790.51855994,
        8838.21626380,
        8885.66208644,
        8932.85372514,
        8979.78893227,
        9026.46551490,
        9072.88133449,
        9119.03430644,
        9164.92239976,
        9210.54363669,
        9255.89609224,
        9300.97789384,
        9345.78722093,
        9390.32230452,
        9434.58142677,
        9478.56292060,
        9522.26516922,
        9565.68660570,
        9608.82571256,
        9651.68102126,
        9694.25111185,
        9736.53461241,
        9778.53019868,
        9820.23659354,
        9861.65256660,
        9902.77693369,
        9943.60855641,
        9984.14634166,
        10024.38924118,
        10064.33625106,
        10103.98641125,
        10143.33880512,
        10182.39255895,
        10221.14684147,
        10259.60086337,
        10297.75387680,
        10335.60517492,
        10373.15409140,
        10410.39999994,
        10447.34231378,
        10483.98048522,
        10520.31400514,
        10556.34240253,
        10592.06524395,
        10627.48213314,
        10662.59271046,
        10697.39665243,
        10731.89367128,
        10766.08351444,
        10799.96596406,
        10833.54083657,
        10866.80798215,
        10899.76728432,
        10932.41865941,
        10964.76205614,
        10996.79745511,
        11028.52486836,
        11059.94433889,
        11091.05594022,
        11121.85977591,
        11152.35597912,
        11182.54471212,
        11212.42616589,
        11242.00055963,
        11271.26814031,
        11300.22918226,
        11328.88398670,
        11357.23288130,
        11385.27621977,
        11413.01438137,
        11440.44777057,
        11467.57681651,
        11494.40197267,
        11520.92371641,
        11547.14254852,
        11573.05899287,
        11598.67359596,
        11623.98692649,
        11648.99957501,
        11673.71215347,
        11698.12529482,
        11722.23965267,
        11746.05590082,
        11769.57473294,
        11792.79686212,
        11815.72302055,
        11838.35395910,
        11860.69044694,
        11882.73327121,
        11904.48323661,
        11925.94116506,
        11947.10789532,
        11967.98428265,
        11988.57119843,
        12008.86952986,
        12028.88017954,
        12048.60406519,
        12068.04211929,
        12087.19528873,
        12106.06453447,
        12124.65083127,
        12142.95516728,
        12160.97854379,
        12178.72197486,
        12196.18648704,
        12213.37311905,
        12230.28292145,
        12246.91695637,
        12263.27629719,
        12279.36202824,
        12295.17524453,
        12310.71705141,
        12325.98856435,
        12340.99090860,
        12355.72521896,
        12370.19263945,
        12384.39432308,
        12398.33143156,
        12412.00513505,
        12425.41661189,
        12438.56704832,
        12451.45763827,
        12464.08958306,
        12476.46409119,
        12488.58237807,
        12500.44566579,
        12512.05518287,
        12523.41216403,
        12534.51784999,
        12545.37348716,
        12555.98032751,
        12566.33962828,
        12576.45265178,
        12586.32066519,
        12595.94494032,
        12605.32675343,
        12614.46738498,
        12623.36811947,
        12632.03024523,
        12640.45505419,
        12648.64384173,
        12656.59790644,
        12664.31854999,
        12671.80707689,
        12679.06479434,
        12686.09301201,
        12692.89304194,
        12699.46619826,
        12705.81379711,
        12711.93715643,
        12717.83759579,
        12723.51643624,
        12728.97500013,
        12734.21461098,
        12739.23659331,
        12744.04227248,
        12748.63297453,
        12753.01002609,
        12757.17475416,
        12761.12848599,
        12764.87254898,
        12768.40827049,
        12771.73697774,
        12774.85999765,
        12777.77865673,
        12780.49428093,
        12783.00819555,
        12785.32172507,
        12787.43619307,
        12789.35292209,
        12791.07323350,
        12792.59844743,
        12793.92988261,
        12795.06885627,
        12796.01668406,
        12796.77467992,
        12797.34415597,
        12797.72642243,
        12797.92278749,
        12797.93455726,
        12797.76303562,
        12797.40952415,
        12796.87532205,
        12796.16172604,
        12795.27003026,
        12794.20152618,
        12792.95750257,
        12791.53924533,
        12789.94803749,
        12788.18515908,
        12786.25188706,
        12784.14949528,
        12781.87925435,
        12779.44243162,
        12776.84029106,
        12774.07409325,
        12771.14509526,
        12768.05455060,
        12764.80370917,
        12761.39381718,
        12757.82611712,
        12754.10184764,
        12750.22224355,
        12746.18853574,
        12742.00195113,
        12737.66371261,
        12733.17503899,
        12728.53714494,
        12723.75124098,
        12718.81853337,
        12713.74022411,
        12708.51751090,
        12703.15158703,
        12697.64364143,
        12691.99485855,
        12686.20641836,
        12680.27949632,
        12674.21526329,
        12668.01488555,
        12661.67952475,
        12655.21033783,
        12648.60847706,
        12641.87508995,
        12635.01131925,
        12628.01830291,
        12620.89717405,
        12613.64906092,
        12606.27508691,
        12598.77637047,
        12591.15402515,
        12583.40915951,
        12575.54287714,
        12567.55627664,
        12559.45045156,
        12551.22649042,
        12542.88547667,
        12534.42848868,
        12525.85659972,
        12517.17087794,
        12508.37238636,
        12499.46218286,
        12490.44132013,
        12481.31084572,
        12472.07180197,
        12462.72522603,
        12453.27214983,
        12443.71360008,
        12434.05059828,
        12424.28416067,
        12414.41529824,
        12404.44501674,
        12394.37431665,
        12384.20419318,
        12373.93563628,
        12363.56963061,
        12353.10715554,
        12342.54918519,
        12331.89668836,
        12321.15062856,
        12310.31196403,
        12299.38164769,
        12288.36062720,
        12277.24984489,
        12266.05023782,
        12254.76273776,
        12243.38827118,
        12231.92775927,
        12220.38211792,
        12208.75225776,
        12197.03908412,
        12185.24349708,
        12173.36639143,
        12161.40865671,
        12149.37117718,
        12137.25483188,
        12125.06049458,
        12112.78903381,
        12100.44131289,
        12088.01818988,
        12075.52051766,
        12062.94914387,
        12050.30491098,
        12037.58865624,
        12024.80121175,
        12011.94340442,
        11999.01605600,
        11986.01998309,
        11972.95599717,
        11959.82490456,
        11946.62750648,
        11933.36459906,
        11920.03697332,
        11906.64541520,
        11893.19070557,
        11879.67362026,
        11866.09493006,
        11852.45540071,
        11838.75579295,
        11824.99686253,
        11811.17936021,
        11797.30403177,
        11783.37161803,
        11769.38285489,
        11755.33847331,
        11741.23919934,
        11727.08575414,
        11712.87885400,
        11698.61921032,
        11684.30752968,
        11669.94451382,
        11655.53085966,
        11641.06725934,
        11626.55440020,
        11611.99296484,
        11597.38363109,
        11582.72707208,
        11568.02395621,
        11553.27494718,
        11538.48070404,
        11523.64188117,
        11508.75912831,
        11493.83309058,
        11478.86440851,
        11463.85371803,
        11448.80165051,
        11433.70883278,
        11418.57588715,
        11403.40343140,
        11388.19207883,
        11372.94243828,
        11357.65511413,
        11342.33070633,
        11326.96981042,
        11311.57301754,
        11296.14091447,
        11280.67408363,
        11265.17310311,
        11249.63854667,
        11234.07098379,
        11218.47097968,
        11202.83909529,
        11187.17588733,
        11171.48190831,
        11155.75770652,
        11140.00382611,
        11124.22080706,
        11108.40918520,
        11092.56949227,
        11076.70225590,
        11060.80799967,
        11044.88724309,
        11028.94050163,
        11012.96828677,
        10996.97110598,
        10980.94946277,
        10964.90385669,
        10948.83478337,
        10932.74273452,
        10916.62819797,
        10900.49165767,
        10884.33359373,
        10868.15448243,
        10851.95479625,
        10835.73500386,
        10819.49557018,
        10803.23695638,
        10786.95961991,
        10770.66401450,
        10754.35059021,
        10738.01979343,
        10721.67206689,
        10705.30784972,
        10688.92757743,
        10672.53168195,
        10656.12059164,
        10639.69473134,
        10623.25452233,
        10606.80038243,
        10590.33272593,
        10573.85196369,
        10557.35850312,
        10540.85274820,
        10524.33509952,
        10507.80595427,
        10491.26570629,
        10474.71474607,
        10458.15346079,
        10441.58223429,
        10425.00144718,
        10408.41147676,
        10391.81269711,
        10375.20547907,
        10358.59019029,
        10341.96719523,
        10325.33685516,
        10308.69952825,
        10292.05556949,
        10275.40533080,
        10258.74916099,
        10242.08740581,
        10225.42040795,
        10208.74850708,
        10192.07203984,
        10175.39133990,
        10158.70673793,
        10142.01856166,
        10125.32713586,
        10108.63278242,
        10091.93582030,
        10075.23656557,
        10058.53533147,
        10041.83242836,
        10025.12816380,
        10008.42284253,
        9991.71676650,
        9975.01023489,
        9958.30354412,
        9941.59698789,
        9924.89085715,
        9908.18544019,
        9891.48102260,
        9874.77788729,
        9858.07631455,
        9841.37658201,
        9824.67896473,
        9807.98373514,
        9791.29116311,
        9774.60151594,
        9757.91505839,
        9741.23205271,
    ]
)

DATA_RAYLEIGH_JEANS_LAW: dict = {
    1667: np.array(
        [
            1.379970796097092e25,
            8.624817475606822e23,
            5.390510922254264e22,
            3.369069326408915e21,
            2.105668329005572e20,
            1.316042705628482e19,
            8.225266910178015e17,
            5.140791818861259e16,
            3.212994886788287e15,
            2.008121804242679e14,
            1.255076127651675e13,
            7.844225797822966e11,
            4.902641123639354e10,
            3.064150702274596e09,
            1.915094188921623e08,
            1.196933868076014e07,
        ]
    ),
    5000: np.array(
        [
            4.139084571376999e25,
            2.586927857110624e24,
            1.616829910694140e23,
            1.010518694183838e22,
            6.315741838648986e20,
            3.947338649155616e19,
            2.467086655722260e18,
            1.541929159826412e17,
            9.637057248915078e15,
            6.023160780571924e14,
            3.764475487857452e13,
            2.352797179910908e12,
            1.470498237444317e11,
            9.190613984026983e09,
            5.744133740016865e08,
            3.590083587510540e07,
        ]
    ),
    10000: np.array(
        [
            8.278169142753998e25,
            5.173855714221249e24,
            3.233659821388281e23,
            2.021037388367675e22,
            1.263148367729797e21,
            7.894677298311232e19,
            4.934173311444520e18,
            3.083858319652825e17,
            1.927411449783016e16,
            1.204632156114385e15,
            7.528950975714905e13,
            4.705594359821815e12,
            2.940996474888635e11,
            1.838122796805397e10,
            1.148826748003373e09,
            7.180167175021081e07,
        ]
    ),
    100000: np.array(
        [
            8.278169142753999e26,
            5.173855714221249e25,
            3.233659821388281e24,
            2.021037388367675e23,
            1.263148367729797e22,
            7.894677298311232e20,
            4.934173311444520e19,
            3.083858319652825e18,
            1.927411449783016e17,
            1.204632156114385e16,
            7.528950975714905e14,
            4.705594359821816e13,
            2.940996474888635e12,
            1.838122796805397e11,
            1.148826748003373e10,
            7.180167175021081e08,
        ]
    ),
    10000000000000000000: np.array(
        [
            8.278169142753998e40,
            5.173855714221249e39,
            3.233659821388280e38,
            2.021037388367675e37,
            1.263148367729797e36,
            7.894677298311232e34,
            4.934173311444520e33,
            3.083858319652825e32,
            1.927411449783016e31,
            1.204632156114385e30,
            7.528950975714904e28,
            4.705594359821815e27,
            2.940996474888635e26,
            1.838122796805397e25,
            1.148826748003373e24,
            7.180167175021080e22,
        ]
    ),
}

DATA_RAYLEIGH_JEANS: NDArrayFloat = np.array(
    [
        2464304.08580116,
        2437112.02495309,
        2410293.99092788,
        2383843.82698718,
        2357755.49430373,
        2332023.06938771,
        2306640.74157597,
        2281602.81058267,
        2256903.68410954,
        2232537.87551423,
        2208500.00153509,
        2184784.78007096,
        2161387.02801446,
        2138301.65913732,
        2115523.68202642,
        2093048.19806916,
        2070870.39948685,
        2048985.56741487,
        2027389.07002836,
        2006076.36071225,
        1985042.97627445,
        1964284.53520105,
        1943796.73595254,
        1923575.35529985,
        1903616.24669927,
        1883915.33870518,
        1864468.63341964,
        1845272.20497799,
        1826322.19806929,
        1807614.82649099,
        1789146.37173673,
        1770913.18161664,
        1752911.66890902,
        1735138.31004297,
        1717589.64381086,
        1700262.27011009,
        1683152.84871331,
        1666258.09806643,
        1649574.79411371,
        1633099.76914923,
        1616829.91069414,
        1600762.16039897,
        1584893.51297047,
        1569221.01512229,
        1553741.76454898,
        1538452.90892266,
        1523351.64491191,
        1508435.21722224,
        1493700.91765764,
        1479146.08420271,
        1464768.10012489,
        1450564.39309625,
        1436532.43433442,
        1422669.73776213,
        1408973.85918499,
        1395442.39548702,
        1382072.98384357,
        1368863.30095106,
        1355811.06227338,
        1342914.02130427,
        1330169.96884561,
        1317576.73230094,
        1305132.17498411,
        1292834.19544248,
        1280680.72679452,
        1268669.73608136,
        1256799.22363196,
        1245067.22244167,
        1233471.79756379,
        1222011.04551379,
        1210683.09368606,
        1199486.09978275,
        1188418.25125442,
        1177477.76475235,
        1166662.88559214,
        1155971.88722837,
        1145403.07074002,
        1134954.76432657,
        1124625.32281429,
        1114413.12717269,
        1104316.58404080,
        1094334.12526312,
        1084464.20743492,
        1074705.31145682,
        1065055.94209833,
        1055514.62757016,
        1046079.91910521,
        1036750.39054792,
        1027524.63795180,
        1018401.27918507,
        1009378.95354415,
        1000456.32137483,
        991632.06370089,
        982904.88186021,
        974273.49714794,
        965736.65046681,
        957293.10198421,
        948941.63079610,
        940681.03459747,
        932510.12935920,
        924427.74901127,
        916432.74513213,
        908523.98664409,
        900700.35951458,
        892960.76646326,
        885304.12667472,
        877729.37551674,
        870235.46426394,
        862821.35982674,
        855486.04448552,
        848228.51562981,
        841047.78550252,
        833942.88094894,
        826912.84317059,
        819956.72748365,
        813073.60308201,
        806262.55280479,
        799522.67290815,
        792853.07284149,
        786252.87502779,
        779721.21464802,
        773257.23942967,
        766860.10943911,
        760528.99687786,
        754263.08588266,
        748061.57232918,
        741923.66363940,
        735848.57859250,
        729835.54713927,
        723883.81021991,
        717992.61958513,
        712161.23762058,
        706388.93717442,
        700675.00138811,
        695018.72353015,
        689419.40683297,
        683876.36433270,
        678388.91871179,
        672956.40214459,
        667578.15614556,
        662253.53142032,
        656981.88771933,
        651762.59369414,
        646595.02675630,
        641478.57293866,
        636412.62675926,
        631396.59108754,
        626429.87701297,
        621511.90371596,
        616642.09834110,
        611819.89587257,
        607044.73901180,
        602316.07805719,
        597633.37078606,
        592996.08233849,
        588403.68510338,
        583855.65860632,
        579351.48939950,
        574890.67095353,
        570472.70355106,
        566097.09418233,
        561763.35644241,
        557471.01043035,
        553219.58264989,
        549008.60591203,
        544837.61923916,
        540706.16777085,
        536613.80267128,
        532560.08103820,
        528544.56581345,
        524566.82569504,
        520626.43505058,
        516722.97383237,
        512856.02749375,
        509025.18690690,
        505230.04828213,
        501470.21308831,
        497745.28797486,
        494054.88469483,
        490398.62002946,
        486776.11571381,
        483186.99836375,
        479630.89940414,
        476107.45499810,
        472616.30597761,
        469157.09777511,
        465729.48035629,
        462333.10815398,
        458967.64000311,
        455632.73907674,
        452328.07282311,
        449053.31290380,
        445808.13513275,
        442592.21941641,
        439405.24969480,
        436246.91388347,
        433116.90381655,
        430014.91519051,
        426940.64750903,
        423893.80402859,
        420874.09170506,
        417881.22114102,
        414914.90653407,
        411974.86562580,
        409060.81965172,
        406172.49329188,
        403309.61462234,
        400471.91506733,
        397659.12935230,
        394870.99545756,
        392107.25457273,
        389367.65105193,
        386651.93236960,
        383959.84907704,
        381291.15475971,
        378645.60599502,
        376022.96231097,
        373422.98614531,
        370845.44280539,
        368290.10042857,
        365756.72994335,
        363245.10503098,
        360755.00208776,
        358286.20018785,
        355838.48104671,
        353411.62898503,
        351005.43089331,
        348619.67619689,
        346254.15682153,
        343908.66715961,
        341583.00403669,
        339276.96667869,
        336990.35667955,
        334722.97796934,
        332474.63678288,
        330245.14162884,
        328034.30325930,
        325841.93463975,
        323667.85091953,
        321511.86940280,
        319373.80951983,
        317253.49279878,
        315150.74283790,
        313065.38527812,
        310997.24777608,
        308946.15997754,
        306911.95349116,
        304894.46186272,
        302893.52054969,
        300908.96689618,
        298940.64010825,
        296988.38122958,
        295052.03311756,
        293131.44041960,
        291226.44954993,
        289336.90866664,
        287462.66764911,
        285603.57807569,
        283759.49320186,
        281930.26793851,
        280115.75883067,
        278315.82403654,
        276530.32330673,
        274759.11796391,
        273002.07088268,
        271259.04646976,
        269529.91064447,
        267814.53081943,
        266112.77588166,
        264424.51617379,
        262749.62347568,
        261087.97098621,
        259439.43330537,
        257803.88641661,
        256181.20766940,
        254571.27576206,
        252973.97072484,
        251389.17390327,
        249816.76794164,
        248256.63676681,
        246708.66557223,
        245172.74080214,
        243648.75013606,
        242136.58247340,
        240636.12791839,
        239147.27776515,
        237669.92448300,
        236203.96170195,
        234749.28419840,
        233305.78788108,
        231873.36977708,
        230451.92801820,
        229041.36182739,
        227641.57150544,
        226252.45841778,
        224873.92498157,
        223505.87465285,
        222148.21191393,
        220800.84226099,
        219463.67219171,
        218136.60919325,
        216819.56173022,
        215512.43923297,
        214215.15208591,
        212927.61161606,
        211649.73008174,
        210381.42066140,
        209122.59744260,
        207873.17541119,
        206633.07044054,
        205402.19928097,
        204180.47954938,
        202967.82971887,
        201764.16910866,
        200569.41787401,
        199383.49699638,
        198206.32827363,
        197037.83431046,
        195877.93850882,
        194726.56505862,
        193583.63892843,
        192449.08585638,
        191322.83234115,
        190204.80563304,
        189094.93372528,
        187993.14534527,
        186899.36994615,
        185813.53769827,
        184735.57948091,
        183665.42687407,
        182603.01215037,
        181548.26826703,
        180501.12885795,
        179461.52822599,
        178429.40133520,
        177404.68380326,
        176387.31189398,
        175377.22250989,
        174374.35318497,
        173378.64207738,
        172390.02796239,
        171408.45022533,
        170433.84885467,
        169466.16443513,
        168505.33814099,
        167551.31172935,
        166604.02753355,
        165663.42845670,
        164729.45796522,
        163802.06008252,
        162881.17938270,
        161966.76098442,
        161058.75054476,
        160157.09425319,
        159261.73882564,
        158372.63149859,
        157489.72002329,
        156612.95266005,
        155742.27817251,
        154877.64582211,
        154019.00536257,
        153166.30703441,
        152319.50155957,
        151478.54013612,
        150643.37443299,
        149813.95658480,
        148990.23918670,
        148172.17528937,
        147359.71839398,
        146552.82244729,
        145751.44183673,
        144955.53138565,
        144165.04634850,
        143379.94240619,
        142600.17566142,
        141825.70263410,
        141056.48025685,
        140292.46587048,
        139533.61721964,
        138779.89244839,
        138031.25009594,
        137287.64909237,
        136549.04875443,
        135815.40878139,
        135086.68925090,
        134362.85061501,
        133643.85369608,
        132929.65968288,
        132220.23012665,
        131515.52693725,
        130815.51237932,
        130120.14906856,
        129429.39996793,
        128743.22838403,
        128061.59796343,
        127384.47268908,
        126711.81687677,
        126043.59517160,
        125379.77254452,
        124720.31428890,
        124065.18601715,
        123414.35365738,
        122767.78345007,
        122125.44194479,
        121487.29599703,
        120853.31276495,
        120223.45970624,
        119597.70457501,
        118976.01541870,
        118358.36057506,
        117744.70866907,
        117135.02861007,
        116529.28958873,
        115927.46107417,
        115329.51281112,
        114735.41481704,
        114145.13737933,
        113558.65105255,
        112975.92665569,
        112396.93526944,
        111821.64823355,
        111250.03714412,
        110682.07385104,
        110117.73045538,
        109556.97930681,
        108999.79300113,
        108446.14437769,
        107896.00651698,
        107349.35273818,
        106806.15659671,
        106266.39188188,
        105730.03261451,
        105197.05304458,
        104667.42764898,
        104141.13112915,
        103618.13840890,
        103098.42463211,
        102581.96516058,
        102068.73557183,
        101558.71165693,
        101051.86941838,
        100548.18506803,
        100047.63502494,
        99550.19591335,
        99055.84456065,
        98564.55799537,
        98076.31344514,
        97591.08833478,
        97108.86028431,
        96629.60710704,
        96153.30680767,
        95679.93758038,
        95209.47780699,
        94741.90605514,
        94277.20107639,
        93815.34180450,
        93356.30735360,
        92900.07701645,
        92446.63026267,
        91995.94673705,
        91548.00625781,
        91102.78881494,
        90660.27456852,
        90220.44384706,
        89783.27714590,
        89348.75512555,
        88916.85861013,
        88487.56858577,
        88060.86619906,
        87636.73275549,
        87215.14971794,
    ]
)


class TestPlanckLaw(unittest.TestCase):
    """
    Define :func:`colour.colorimetry.blackbody.planck_law` definition unit
    tests methods.
    """

    def test_planck_law(self):
        """Test :func:`colour.colorimetry.blackbody.planck_law` definition."""

        wavelengths = 2 ** np.arange(0, 16, 1) * 1e-9
        for temperature, radiance in sorted(DATA_PLANCK_LAW.items()):
            np.testing.assert_allclose(
                planck_law(wavelengths, temperature),
                radiance,
                rtol=0.0000001,
                atol=0.0000001,
                verbose=False,
            )

    def test_n_dimensional_planck_law(self):
        """
        Test :func:`colour.colorimetry.blackbody.planck_law` definition
        n-dimensional arrays support.
        """

        wl = 500 * 1e-9
        p = planck_law(wl, 5500)

        wl = np.tile(wl, 6)
        p = np.tile(p, 6)
        np.testing.assert_array_almost_equal(planck_law(wl, 5500), p)

        wl = np.reshape(wl, (2, 3))
        # The "colour.colorimetry.planck_law" definition behaviour with
        # n-dimensional arrays is unusual.
        # p = np.np.reshape(p, (2, 3))
        np.testing.assert_array_almost_equal(planck_law(wl, 5500), p)

        wl = np.reshape(wl, (2, 3, 1))
        # The "colour.colorimetry.planck_law" definition behaviour with
        # n-dimensional arrays is unusual.
        # p = np.reshape(p, (2, 3, 1))
        np.testing.assert_array_almost_equal(planck_law(wl, 5500), p)

        # The "colour.colorimetry.planck_law" definition behaviour with
        # n-dimensional arrays is unusual.
        p = planck_law(500 * 1e-9, [5000, 5500, 6000])
        p = np.tile(p, (6, 1))
        np.testing.assert_array_almost_equal(
            planck_law(wl, [5000, 5500, 6000]), p
        )

    def test_raise_exception_planck_law(self):
        """
        Test :func:`colour.colorimetry.blackbody.planck_law` definition
        raised exception.
        """

        for wavelength in [-1.0, 0.0, -np.inf, np.nan]:
            self.assertRaises(AssertionError, planck_law, wavelength, 5500)

    @ignore_numpy_errors
    def test_nan_planck_law(self):
        """
        Test :func:`colour.colorimetry.blackbody.planck_law` definition nan
        support.
        """

        # NOTE: Only testing infinity support as
        cases = [1.0, np.inf]
        cases = np.array(list(set(product(cases, repeat=3))))
        planck_law(cases, cases)


class TestSdBlackbody(unittest.TestCase):
    """
    Define :func:`colour.colorimetry.blackbody.sd_blackbody` definition unit
    tests methods.
    """

    def test_sd_blackbody(self):
        """Test :func:`colour.colorimetry.blackbody.sd_blackbody` definition."""

        np.testing.assert_allclose(
            sd_blackbody(5000, SpectralShape(360, 830, 1)).values,
            DATA_BLACKBODY,
            rtol=0.0000001,
            atol=0.0000001,
        )


class TestRayleighJeansLaw(unittest.TestCase):
    """
    Define :func:`colour.colorimetry.blackbody.rayleigh_jeans_law` definition unit
    tests methods.
    """

    def test_rayleigh_jeans_law(self):
        """
        Test :func:`colour.colorimetry.blackbody.rayleigh_jeans_law`
        definition.
        """

        wavelengths = 2 ** np.arange(0, 16, 1) * 1e-9
        for temperature, radiance in sorted(DATA_RAYLEIGH_JEANS_LAW.items()):
            np.testing.assert_allclose(
                rayleigh_jeans_law(wavelengths, temperature),
                radiance,
                rtol=0.0000001,
                atol=0.0000001,
                verbose=False,
            )

    def test_n_dimensional_rayleigh_jeans_law(self):
        """
        Test :func:`colour.colorimetry.blackbody.rayleigh_jeans_law` definition
        n-dimensional arrays support.
        """

        wl = 500 * 1e-9
        p = rayleigh_jeans_law(wl, 5500)

        wl = np.tile(wl, 6)
        p = np.tile(p, 6)
        np.testing.assert_array_almost_equal(rayleigh_jeans_law(wl, 5500), p)

        wl = np.reshape(wl, (2, 3))
        # The "colour.colorimetry.rayleigh_jeans_law" definition behaviour with
        # n-dimensional arrays is unusual.
        # p = np.np.reshape(p, (2, 3))
        np.testing.assert_array_almost_equal(rayleigh_jeans_law(wl, 5500), p)

        wl = np.reshape(wl, (2, 3, 1))
        # The "colour.colorimetry.rayleigh_jeans_law" definition behaviour with
        # n-dimensional arrays is unusual.
        # p = np.reshape(p, (2, 3, 1))
        np.testing.assert_array_almost_equal(rayleigh_jeans_law(wl, 5500), p)

        # The "colour.colorimetry.rayleigh_jeans_law" definition behaviour with
        # n-dimensional arrays is unusual.
        p = rayleigh_jeans_law(500 * 1e-9, [5000, 5500, 6000])
        p = np.tile(p, (6, 1))
        np.testing.assert_array_almost_equal(
            rayleigh_jeans_law(wl, [5000, 5500, 6000]), p
        )

    @ignore_numpy_errors
    def test_nan_rayleigh_jeans_law(self):
        """
        Test :func:`colour.colorimetry.blackbody.rayleigh_jeans_law` definition
        nan support.
        """

        cases = [-1.0, 0.0, 1.0, -np.inf, np.inf, np.nan]
        cases = np.array(list(set(product(cases, repeat=3))))
        rayleigh_jeans_law(cases, cases)


class TestSdRayleighJeans(unittest.TestCase):
    """
    Define :func:`colour.colorimetry.blackbody.sd_rayleigh_jeans` definition unit
    tests methods.
    """

    def test_sd_rayleigh_jeans(self):
        """
        Test :func:`colour.colorimetry.blackbody.sd_rayleigh_jeans`
        definition.
        """

        np.testing.assert_allclose(
            sd_rayleigh_jeans(5000, SpectralShape(360, 830, 1)).values,
            DATA_RAYLEIGH_JEANS,
            rtol=0.0000001,
            atol=0.0000001,
        )


if __name__ == "__main__":
    unittest.main()
