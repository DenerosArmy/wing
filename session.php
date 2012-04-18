
<?php
    require_once 'API_Config.php';
    require_once 'OpenTokSDK.php';
    require_once 'SessionPropertyConstants.php';

    $apiObj = new OpenTokSDK(API_Config::API_KEY, API_Config::API_SECRET);

    $session = $apiObj->create_session($_SERVER["REMOTE_ADDR"], 
        array(SessionPropertyConstants::P2P_PREFERENCE=>"enabled"));
    echo $session->getSessionId();
?>
<script src="http://staging.tokbox.com/v0.91/js/TBmin.js"></script>

<iframe width="640" height="480" style="border:none" src=
"http://api.dabbleboard.com/api/iframe?dev_id=sumukh1&user_id=cs61&user_key=cs61&drawing_user_id=cs61&drawing_id=0&drawing_key=cs61&width=640&height=480"
></iframe>

<br>
</iframe>
