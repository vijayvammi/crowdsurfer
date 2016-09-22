# -*- coding: utf-8 -*-

import scrape_crowdcube as sc
content = '''<div class="pitch">

<article id="pitch-21198"
        data-new-pitch-page="1"
         onclick="crowdcube.sendPitchOrder(
    'Investment Opportunites',
    21198,
    'World of Zing', 
    2,
    'equity'
    );" >

    <a href="https://www.crowdcube.com/investment/world-of-zing-21198">

        <figure class="pitch__coverImage">

                            <picture>
                    <source media="(min-width: 1001px)" srcset="https://images.crowdcube.com/unsafe/780x175/filters:max_bytes(20000):format(jpeg):quality(40)/https://files-crowdcube-com.s3.amazonaws.com/opportunity_images/21198/201608/banner_1500x375_lr_7b05bc1fe15604bd8b74ec25f980a38d.jpg" />
                    <source media="(min-width: 641px) and (max-width: 1000px)" srcset="https://images.crowdcube.com/unsafe/1000x350/filters:max_bytes(20000):format(jpeg):quality(40)/https://files-crowdcube-com.s3.amazonaws.com/opportunity_images/21198/201608/banner_1500x375_lr_7b05bc1fe15604bd8b74ec25f980a38d.jpg" />
                    <source media="(max-width: 640px)" srcset="https://images.crowdcube.com/unsafe/640x400/filters:max_bytes(20000):format(jpeg):quality(40)/https://files-crowdcube-com.s3.amazonaws.com/opportunity_images/21198/201608/banner_1500x375_lr_7b05bc1fe15604bd8b74ec25f980a38d.jpg" />
                    <img src="https://images.crowdcube.com/unsafe/1000x625/filters:max_bytes(20000):format(jpeg):quality(40)/https://files-crowdcube-com.s3.amazonaws.com/opportunity_images/21198/201608/banner_1500x375_lr_7b05bc1fe15604bd8b74ec25f980a38d.jpg" alt="World of Zing" />
                </picture>
            
        </figure>

    </a>

    
    <section class="pitch__detail">

        <figure class="pitch__logo">

            <a href="https://www.crowdcube.com/investment/world-of-zing-21198">

                <img src="https://images.crowdcube.com/unsafe/fit-in/100x76/filters:max_bytes(5000)/https://files-crowdcube-com.s3.amazonaws.com/files/pitch_pics/original/201608/woz-logo-orange-pioneers_sq_9c5865e799a09e8a527543a5ce86aebf.jpg" alt=""/>

            </a>

        </figure>

        <h2 class="pitch__title"><a href="https://www.crowdcube.com/investment/world-of-zing-21198" title="World of Zing">World of Zing</a></h2>

                    <ul class="pitch__tax tax">
                                    <li class="tax__item">EIS </li>
                                            </ul>
        
        <p class="pitch__description">
            <a href="https://www.crowdcube.com/investment/world-of-zing-21198">World of Zing specializes in bringing an innovative range of foods and drinks to their customers through developing in-house products and collaborating with exceptional artisan’s. Since launching in 2014 they have expanding their product range offering spices, sauces, cocktails and more.</a>
        </p>

        <div class="pitch__progress">

            <div class="pitchProgress  ">

                <span class="pitchProgress__percentage" style="width: 1%;">1%</span>

                                                        <div class="pitchProgress__bar" style="width: 1%;"></div>
                
                
            </div>

            <div class="pitchProgress__stats">
                <span class="pitchProgress__figure">£1,250</span>
                <span class="pitchProgress__label">raised</span>
            </div>

        </div>

        <ul class="pitch__stats">

            <li class="pitch__stat">
                <span class="pitch__statLabel">Target</span>
                <span class="pitch__statFigure">£150,000</span>
            </li>

            <li class="pitch__stat">
                <span class="pitch__statLabel">Equity</span>
                <span class="pitch__statFigure">15.00%</span>
            </li>

            <li class="pitch__stat">
                <span class="pitch__statLabel">Investors</span>
                <span class="pitch__statFigure">11</span>
            </li>

            <li class="pitch__stat ">
                                    <span class="pitch__statLabel">Days left</span>
                    <span class="pitch__statFigure">28</span>
                            </li>

        </ul>

    </section>

    <script>

        var pitch21198 = {
            pitch_id        : 21198,
            pitch_name      : "World of Zing",
            pitch_type      : "equity",
            pitch_target    : "150000",
            days_remaining  : 28,
            progress        : 1,
            investors       : 11,
            current_amount  : 1250,
            equity_offered  : 15.00,
            list_position   : 2
        };
    </script>

</article>

                                                <div class="follow-pitch clearfix">
    <a href="https://www.crowdcube.com/login?redirect_to=L2ludmVzdG1lbnRz"
    data-pitch-id="21198"
    data-pitch-name="World of Zing"
    data-pitch-following="false"
    class="cc-btnTag
    linkFollow "
    onclick="crowdcube.trackFollow(
        this,
        21198,
        null,
        1,
        1250,
        11,
        15.00
        );">
        <span class="unfollowedText" >Follow</span>
        <span class="followedText" style="display:none;">Following</span>
        <span class="followError" style="display:none;">An error occured. Please try again.</span>
    </a>
</div>

            </div>
'''
def test_extract_with_errors(monkeypatch):
    class my_response:
        @staticmethod
        def getcode():
            return 400
    def mockreturn(req):
        return my_response
    monkeypatch.setattr(sc.urllib2, 'urlopen', mockreturn)
    invs = sc.extract()
    assert len(invs) == 0

def test_extract_with_dummy(monkeypatch):
    class my_response:
        @staticmethod
        def getcode():
            return 200
        @staticmethod
        def read():
            return content    
    def mockreturn(req):
        return my_response
    monkeypatch.setattr(sc.urllib2, 'urlopen', mockreturn) 
    invs = sc.extract()
    assert len(invs) == 1     

    
