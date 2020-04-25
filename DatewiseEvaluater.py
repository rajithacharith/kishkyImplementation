import csv


def evaluateDatewise(filePath, results):
    alignedEng = []
    alignedSin = []
    # print(len(results))
    with open(filePath) as csvfile:
        csvReader = csv.reader(csvfile, delimiter = "|")
        for row in csvReader:
            alignedEng.append(row[0].strip().replace("json", "raw"))
            alignedSin.append(row[2].strip().replace("json", "raw"))
    totcounter = 0
    alignedcounter = 0
    # print(len(alignedEng))
    # print(len(alignedSin))
    for result in results:
        if result["a"] in alignedEng:
            totcounter = totcounter + 1
            if result["b"] == alignedSin[alignedEng.index(result["a"])]:
                alignedcounter = alignedcounter + 1
        # else:
        #     print(result["a"], result["b"])
    return alignedcounter, totcounter


# dec02 = [{'a': '61537.raw', 'b': '7963295.raw', 'distance': 0.7493572963347446}, {'a': '4069341.raw', 'b': '2943463.raw', 'distance': 0.7768796219814955}, {'a': '5732352.raw', 'b': '9477195.raw', 'distance': 0.7805795641710755}, {'a': '9067891.raw', 'b': '7305178.raw', 'distance': 0.8160621503988901}, {'a': '7452149.raw', 'b': '6710064.raw', 'distance': 0.8340638237893516}, {'a': '7324962.raw', 'b': '2253312.raw', 'distance': 0.8400080748488533}, {'a': '4579849.raw', 'b': '6211032.raw', 'distance': 0.8546542216522433}, {'a': '7609580.raw', 'b': '6651203.raw', 'distance': 0.8622197493722167}, {'a': '4939164.raw', 'b': '5894100.raw', 'distance': 0.8790986791803523}, {'a': '4871280.raw', 'b': '9338104.raw', 'distance': 0.8987836629332918}, {'a': '3964955.raw', 'b': '7303556.raw', 'distance': 0.915585607677311}, {'a': '2501843.raw', 'b': '855795.raw', 'distance': 0.9263535472176697}, {'a': '7118202.raw', 'b': '2768830.raw', 'distance': 0.9277730720482535}, {'a': '5295162.raw', 'b': '7549796.raw', 'distance': 0.9362687903423955}, {'a': '40400.raw', 'b': '9344668.raw', 'distance': 0.9503866933990446}, {'a': '4858245.raw', 'b': '7943627.raw', 'distance': 0.9509604328708675}, {'a': '4877000.raw', 'b': '3441656.raw', 'distance': 0.9705460759231547}, {'a': '1210734.raw', 'b': '336457.raw', 'distance': 0.989308184436383}, {'a': '6955899.raw', 'b': '3174813.raw', 'distance': 0.9970918074709714}, {'a': '1378412.raw', 'b': '7750108.raw', 'distance': 1.0024355184349547}, {'a': '7539642.raw', 'b': '4891694.raw', 'distance': 1.004362611990908}, {'a': '6310286.raw', 'b': '3677833.raw', 'distance': 1.007261681111304}, {'a': '3206869.raw', 'b': '6288639.raw', 'distance': 1.0092060281799522}, {'a': '4971346.raw', 'b': '7433488.raw', 'distance': 1.0098538955598206}, {'a': '2561133.raw', 'b': '8747943.raw', 'distance': 1.0182127388747964}, {'a': '6246395.raw', 'b': '6315499.raw', 'distance': 1.0345733723723698}, {'a': '4625192.raw', 'b': '5838413.raw', 'distance': 1.0714468688325314}, {'a': '3787845.raw', 'b': '4870369.raw', 'distance': 1.1447809488154113}]
# dec04 = [{'a': '1522942.raw', 'b': '5848237.raw', 'distance': 0.7464038049903783}, {'a': '2435813.raw', 'b': '531155.raw', 'distance': 0.7764475357556728}, {'a': '151726.raw', 'b': '4248212.raw', 'distance': 0.7828504088173412}, {'a': '8407782.raw', 'b': '8129003.raw', 'distance': 0.7861082800137583}, {'a': '5880609.raw', 'b': '6562004.raw', 'distance': 0.7966055932660381}, {'a': '2746562.raw', 'b': '1256392.raw', 'distance': 0.8266193842235082}, {'a': '4755774.raw', 'b': '9667496.raw', 'distance': 0.846120736825055}, {'a': '2297325.raw', 'b': '3245021.raw', 'distance': 0.849400233477354}, {'a': '2811207.raw', 'b': '4324484.raw', 'distance': 0.8603053514680803}, {'a': '8570968.raw', 'b': '8407300.raw', 'distance': 0.8862018486722997}, {'a': '1985848.raw', 'b': '7203215.raw', 'distance': 0.8867247385338536}, {'a': '3524859.raw', 'b': '7816986.raw', 'distance': 0.8890577752151941}, {'a': '6647826.raw', 'b': '1923285.raw', 'distance': 0.8895999836918689}, {'a': '6687305.raw', 'b': '7071428.raw', 'distance': 0.890284739364051}, {'a': '5593624.raw', 'b': '417748.raw', 'distance': 0.8962527035516142}, {'a': '7894328.raw', 'b': '4192688.raw', 'distance': 0.9081044223336946}, {'a': '8424977.raw', 'b': '4917088.raw', 'distance': 0.9181639181759017}, {'a': '6885298.raw', 'b': '476077.raw', 'distance': 0.9203237811801804}, {'a': '8076061.raw', 'b': '9071846.raw', 'distance': 0.9206038861358542}, {'a': '6515982.raw', 'b': '5729045.raw', 'distance': 0.9223232175057489}, {'a': '9498822.raw', 'b': '9159244.raw', 'distance': 0.922696796796593}, {'a': '8920510.raw', 'b': '7282707.raw', 'distance': 0.9230807462424943}, {'a': '3046391.raw', 'b': '673984.raw', 'distance': 0.9273822672679042}, {'a': '1761970.raw', 'b': '7850895.raw', 'distance': 0.9288897286401734}, {'a': '4963810.raw', 'b': '753868.raw', 'distance': 0.9335279141282349}, {'a': '2211346.raw', 'b': '4564203.raw', 'distance': 0.9355003000261002}, {'a': '3937098.raw', 'b': '145649.raw', 'distance': 0.9365276294696891}, {'a': '4083401.raw', 'b': '9950835.raw', 'distance': 0.9389299447880983}, {'a': '6096723.raw', 'b': '7133161.raw', 'distance': 0.9416085629312839}, {'a': '9959002.raw', 'b': '7662243.raw', 'distance': 0.9452471076775857}, {'a': '3263055.raw', 'b': '652267.raw', 'distance': 0.9467062678062571}, {'a': '1620807.raw', 'b': '9972686.raw', 'distance': 0.9484387635296966}, {'a': '14009.raw', 'b': '3982239.raw', 'distance': 0.9485953989435597}, {'a': '1444065.raw', 'b': '8784991.raw', 'distance': 0.9558253550201439}, {'a': '9280018.raw', 'b': '4713912.raw', 'distance': 0.9561342383007041}, {'a': '4920461.raw', 'b': '5015277.raw', 'distance': 0.9567863009411057}, {'a': '3909624.raw', 'b': '4238912.raw', 'distance': 0.9583246694396468}, {'a': '5030377.raw', 'b': '1544013.raw', 'distance': 0.9671855766227788}, {'a': '8403133.raw', 'b': '4294412.raw', 'distance': 0.973325652701336}, {'a': '3865953.raw', 'b': '1967654.raw', 'distance': 0.9747288546491638}, {'a': '6827967.raw', 'b': '5863381.raw', 'distance': 0.9803383836402227}, {'a': '5437261.raw', 'b': '1173218.raw', 'distance': 0.9826680341727669}, {'a': '4725397.raw', 'b': '8859715.raw', 'distance': 0.9829924868539048}, {'a': '570720.raw', 'b': '6188088.raw', 'distance': 0.9873690369299373}, {'a': '6277617.raw', 'b': '2914532.raw', 'distance': 0.9923221642059111}, {'a': '8400333.raw', 'b': '3733970.raw', 'distance': 0.9927111563521952}, {'a': '6666223.raw', 'b': '3702776.raw', 'distance': 0.9933038497412645}, {'a': '8189360.raw', 'b': '2586747.raw', 'distance': 0.9944236682606978}, {'a': '3717862.raw', 'b': '9408246.raw', 'distance': 0.9996091261307085}, {'a': '743962.raw', 'b': '1799682.raw', 'distance': 1.000519428662235}, {'a': '854489.raw', 'b': '9344844.raw', 'distance': 1.001172790852726}, {'a': '6184268.raw', 'b': '1654901.raw', 'distance': 1.0031216588232579}, {'a': '72281.raw', 'b': '9349254.raw', 'distance': 1.0074826578022176}, {'a': '765583.raw', 'b': '4612145.raw', 'distance': 1.008367794555622}, {'a': '4674941.raw', 'b': '5954728.raw', 'distance': 1.010804044401199}, {'a': '599146.raw', 'b': '8785972.raw', 'distance': 1.0108769930802382}, {'a': '7730051.raw', 'b': '6830222.raw', 'distance': 1.0171396183173587}, {'a': '4576941.raw', 'b': '1220730.raw', 'distance': 1.0207111791700954}, {'a': '5274694.raw', 'b': '9046860.raw', 'distance': 1.03303461006221}, {'a': '6021115.raw', 'b': '3656575.raw', 'distance': 1.0364451100965877}, {'a': '168182.raw', 'b': '2931994.raw', 'distance': 1.0407061307814771}, {'a': '1432385.raw', 'b': '2481240.raw', 'distance': 1.0596654666494314}, {'a': '6297700.raw', 'b': '8243239.raw', 'distance': 1.0760244161442785}, {'a': '1106305.raw', 'b': '9774273.raw', 'distance': 1.1499337483536114}]
# dec05 = [{'a': '4786709.raw', 'b': '4560205.raw', 'distance': 0.685299720249924}, {'a': '7394112.raw', 'b': '2426010.raw', 'distance': 0.7762358359522645}, {'a': '143148.raw', 'b': '4773742.raw', 'distance': 0.7850590670810026}, {'a': '4881407.raw', 'b': '7365195.raw', 'distance': 0.7865249386670023}, {'a': '6291984.raw', 'b': '504128.raw', 'distance': 0.8004675572653128}, {'a': '3622377.raw', 'b': '577573.raw', 'distance': 0.8011206413962338}, {'a': '8388463.raw', 'b': '7809901.raw', 'distance': 0.8030924952419979}, {'a': '9335801.raw', 'b': '9568756.raw', 'distance': 0.8048471128486329}, {'a': '9240303.raw', 'b': '3645980.raw', 'distance': 0.8071292451524007}, {'a': '7346788.raw', 'b': '5621805.raw', 'distance': 0.8144446287446692}, {'a': '2827133.raw', 'b': '9991008.raw', 'distance': 0.8221695863101137}, {'a': '9213603.raw', 'b': '363219.raw', 'distance': 0.8248256310865871}, {'a': '3011605.raw', 'b': '2780793.raw', 'distance': 0.8331266479630028}, {'a': '5191189.raw', 'b': '9590960.raw', 'distance': 0.8333691232056364}, {'a': '7040811.raw', 'b': '3883513.raw', 'distance': 0.8346073159468146}, {'a': '78070.raw', 'b': '3604602.raw', 'distance': 0.8498363228554421}, {'a': '6830022.raw', 'b': '5234529.raw', 'distance': 0.8505811519241313}, {'a': '6764861.raw', 'b': '3023080.raw', 'distance': 0.8691853609256474}, {'a': '9413008.raw', 'b': '1111322.raw', 'distance': 0.870673578207499}, {'a': '5180414.raw', 'b': '883794.raw', 'distance': 0.8713377305053905}, {'a': '1500239.raw', 'b': '1327263.raw', 'distance': 0.871398174211359}, {'a': '9419380.raw', 'b': '9316729.raw', 'distance': 0.8763839486397218}, {'a': '3811078.raw', 'b': '3803440.raw', 'distance': 0.8797918802329666}, {'a': '7840289.raw', 'b': '6536938.raw', 'distance': 0.8868305322397437}, {'a': '1975040.raw', 'b': '478693.raw', 'distance': 0.8908901647597118}, {'a': '1038930.raw', 'b': '3943406.raw', 'distance': 0.8935539833862394}, {'a': '9906772.raw', 'b': '5599624.raw', 'distance': 0.8973834483261242}, {'a': '958282.raw', 'b': '4076809.raw', 'distance': 0.900928930076984}, {'a': '9580366.raw', 'b': '9143484.raw', 'distance': 0.9025307398922038}, {'a': '8558800.raw', 'b': '2734971.raw', 'distance': 0.9046454029263189}, {'a': '5830196.raw', 'b': '7919016.raw', 'distance': 0.9107232033640722}, {'a': '1274145.raw', 'b': '1642481.raw', 'distance': 0.9142503242741444}, {'a': '7227704.raw', 'b': '8517266.raw', 'distance': 0.9207876760785172}, {'a': '8889033.raw', 'b': '5875091.raw', 'distance': 0.9220176070746693}, {'a': '545590.raw', 'b': '2514199.raw', 'distance': 0.9227159399348898}, {'a': '2624516.raw', 'b': '9194766.raw', 'distance': 0.9244383146817035}, {'a': '5094466.raw', 'b': '5621667.raw', 'distance': 0.9272726423654037}, {'a': '1221130.raw', 'b': '5903506.raw', 'distance': 0.9287320803249058}, {'a': '4055343.raw', 'b': '3691841.raw', 'distance': 0.9301315855163131}, {'a': '2656486.raw', 'b': '3586692.raw', 'distance': 0.9389543506852436}, {'a': '6341878.raw', 'b': '7275962.raw', 'distance': 0.9417187546984168}, {'a': '8961145.raw', 'b': '556790.raw', 'distance': 0.9422894401682747}, {'a': '690315.raw', 'b': '9517286.raw', 'distance': 0.9442280849972786}, {'a': '4786701.raw', 'b': '9099367.raw', 'distance': 0.9443554146422279}, {'a': '6781033.raw', 'b': '4223260.raw', 'distance': 0.9447671327677168}, {'a': '4295336.raw', 'b': '9888093.raw', 'distance': 0.9457968498930323}, {'a': '2341720.raw', 'b': '9330410.raw', 'distance': 0.9461810800818005}, {'a': '185027.raw', 'b': '8944389.raw', 'distance': 0.9485597035882004}, {'a': '8501760.raw', 'b': '6287725.raw', 'distance': 0.9487117101249527}, {'a': '4393549.raw', 'b': '7228991.raw', 'distance': 0.9488445098425985}, {'a': '4655866.raw', 'b': '436788.raw', 'distance': 0.9495868823644121}, {'a': '6671900.raw', 'b': '2251014.raw', 'distance': 0.9517926190808466}, {'a': '9796913.raw', 'b': '745088.raw', 'distance': 0.9532171922321748}, {'a': '1133599.raw', 'b': '7674576.raw', 'distance': 0.9555057336983231}, {'a': '9111263.raw', 'b': '5905653.raw', 'distance': 0.9597002464182236}, {'a': '6804651.raw', 'b': '9408549.raw', 'distance': 0.9617078236911607}, {'a': '8911588.raw', 'b': '6798026.raw', 'distance': 0.9620422198414741}, {'a': '9331925.raw', 'b': '1690813.raw', 'distance': 0.9639285119667731}, {'a': '5194657.raw', 'b': '248840.raw', 'distance': 0.9647241065361366}, {'a': '1777821.raw', 'b': '6790222.raw', 'distance': 0.9655077582930451}, {'a': '3545654.raw', 'b': '3534040.raw', 'distance': 0.9688436846938294}, {'a': '5936215.raw', 'b': '7801952.raw', 'distance': 0.9728550226324132}, {'a': '7039035.raw', 'b': '5586995.raw', 'distance': 0.9739852865453592}, {'a': '7078468.raw', 'b': '6318248.raw', 'distance': 0.974155871136552}, {'a': '482378.raw', 'b': '9006747.raw', 'distance': 0.9775389482028644}, {'a': '3306622.raw', 'b': '2241174.raw', 'distance': 0.9776082646595585}, {'a': '6561606.raw', 'b': '8836666.raw', 'distance': 0.9805110834755943}, {'a': '4480358.raw', 'b': '9852757.raw', 'distance': 0.981624755624605}, {'a': '3134508.raw', 'b': '5266787.raw', 'distance': 0.9837756460805548}, {'a': '7235373.raw', 'b': '4796983.raw', 'distance': 0.9881381310293369}, {'a': '4774599.raw', 'b': '7532295.raw', 'distance': 0.9951836228206805}, {'a': '1581228.raw', 'b': '3977000.raw', 'distance': 1.001048921620352}, {'a': '4420649.raw', 'b': '2820290.raw', 'distance': 1.0055650767292086}, {'a': '3874815.raw', 'b': '8813030.raw', 'distance': 1.006177381706624}, {'a': '6062970.raw', 'b': '5563845.raw', 'distance': 1.0079235806362505}, {'a': '7908426.raw', 'b': '8487456.raw', 'distance': 1.0092785712899106}, {'a': '4328110.raw', 'b': '9770935.raw', 'distance': 1.020334346544534}, {'a': '3826824.raw', 'b': '1214131.raw', 'distance': 1.0251612300868362}, {'a': '5111478.raw', 'b': '7350299.raw', 'distance': 1.0293243670432304}, {'a': '6441069.raw', 'b': '1282806.raw', 'distance': 1.0338770508321482}, {'a': '7496411.raw', 'b': '9329658.raw', 'distance': 1.0351842043662332}, {'a': '6070834.raw', 'b': '2266155.raw', 'distance': 1.0369495399341317}, {'a': '1777665.raw', 'b': '2738892.raw', 'distance': 1.0389471845227922}, {'a': '6617151.raw', 'b': '5409895.raw', 'distance': 1.0464684931041828}, {'a': '4300757.raw', 'b': '2100204.raw', 'distance': 1.0529528611955064}, {'a': '1767966.raw', 'b': '4227433.raw', 'distance': 1.0673704140760876}, {'a': '4890.raw', 'b': '265171.raw', 'distance': 1.071356729827112}, {'a': '2196927.raw', 'b': '8014480.raw', 'distance': 1.0777780865011293}, {'a': '2446211.raw', 'b': '4629901.raw', 'distance': 1.089087793939589}, {'a': '5285202.raw', 'b': '7429903.raw', 'distance': 1.094011748871147}, {'a': '2057139.raw', 'b': '4792667.raw', 'distance': 1.0967862945104805}, {'a': '5705463.raw', 'b': '9518471.raw', 'distance': 1.101265516445582}, {'a': '1364797.raw', 'b': '2385902.raw', 'distance': 1.107774389550067}, {'a': '6204528.raw', 'b': '7354560.raw', 'distance': 1.1088151838721299}, {'a': '3873993.raw', 'b': '9395440.raw', 'distance': 1.1233067495016915}, {'a': '4100160.raw', 'b': '1372168.raw', 'distance': 1.1507047658286442}, {'a': '4360401.raw', 'b': '2106608.raw', 'distance': 1.181716033334135}]
# evaluateDatewise("/home/dilan/Private/Projects/FYP/Training Data/Newsfirst/Newsfirst_english_sinhala.txt", dec05)