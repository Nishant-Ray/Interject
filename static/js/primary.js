function questionLink(questionBox) {
    var question = questionBox.childNodes[1].innerHTML;
    var formattedQuestion = "";
    
    for (let i = 0; i < question.length; i++) {
        var char = question.charAt(i);
        
        if (char === ' ') {
            char = '_';
        }

        formattedQuestion += char;
    }
    
    if(window.location.href.includes("offline")) {
        window.open('/side:offline:' + formattedQuestion, '_self');
    } else {
        window.open('/side:online:' + formattedQuestion, '_self');
    }
    
}

function selectSide(side) {
    var url = window.location.href;
    
    if(url.includes("online")) {
        var question = url.substring(url.indexOf(":online:") + 8);
        window.open('/findplayer:' + side + ":" + question, '_self');

    } else {
        var question = url.substring(url.indexOf(":offline:") + 9);
        window.open('/offline:' + side + ":" + question, '_self');
    }
}

function cancelQueue() {
    var url = window.location.href;
    var question;

    if(url.includes('yes')) {
        question = url.substring(url.indexOf("yes:") + 4);
    } else {
        question = url.substring(url.indexOf("no:") + 3);
    }
    

    window.open('/side:online:' + question, '_self');
}

function checkQueue() {
    var url = window.location.href;
    var side;

    if(url.includes('yes')) {
        side = "yes";
        question = url.substring(url.indexOf("yes:") + 4);
    } else {
        side = "no";
        question = url.substring(url.indexOf("no:") + 3);
    }

    setTimeout(function() {
        console.log("repeat");
        window.open('/findplayer:' + side + ":" + question, '_self');
    }, 2000);
}

function loadArguments(userArgument, oppArgument, oppName) {
    console.log("user: " + userArgument + ", opp: " + oppArgument);

    if(userArgument != "" && userArgument != null) {
        
        document.getElementsByClassName("argument-form")[0].style.display = "none";
        
        var userPost = document.getElementById("userPost");
        userPost.style.display = "block";
        
        userPost.getElementsByClassName("post-author")[0].innerHTML = "You<span class='post-time'>" + (new Date()).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) + "</span>";
        userPost.getElementsByClassName("post-content")[0].innerHTML = userArgument;

        if(oppArgument != "" && oppArgument != null) {
            document.getElementsByClassName("opponent-wait")[0].style.display = "none";

            var oppPost = document.getElementById("opponentPost");
            oppPost.style.display = "block";
            
            oppPost.getElementsByClassName("post-author")[0].innerHTML = oppName + "<span class='post-time'>" + (new Date()).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) + "</span>";
            oppPost.getElementsByClassName("post-content")[0].innerHTML = oppArgument;

        }

    }

}

function replyToPost(replyButton) {

    var makeReplyDiv = replyButton.parentElement.getElementsByClassName("make-reply")[0];
    var replyDiv = replyButton.parentElement.getElementsByClassName("reply-div")[0];

    if(makeReplyDiv.style.display == "block") {

        makeReplyDiv.style.display = "none";

        if(replyDiv.style.padding == "30px 40px") {
            
            replyDiv.style.padding = "0";
            replyDiv.style.marginBottom = "0";
            replyDiv.style.marginTop = "0";
        }

    } else {
        
        makeReplyDiv.style.display = "block";

        if(replyDiv.style.padding != "30px 40px") {
            
            replyDiv.style.padding = "30px 40px";
            replyDiv.style.marginBottom = "-30px";
            replyDiv.style.marginTop = "20px";
        }

    }

}

function submitReply(submitButton) {
    
    var replyDiv = submitButton.parentElement.parentElement.parentElement;
    
    if(replyDiv.style.padding != "30px 40px") {
        replyDiv.style.padding = "30px 40px";
        replyDiv.style.marginBottom = "-30px";
        replyDiv.style.marginTop = "20px";
    }

    var temp = document.getElementsByTagName("template")[0];
    var clone = temp.content.cloneNode(true); // reply template
    
    var replyDivClone = clone.childNodes[1];

    var authorText = replyDivClone.getElementsByClassName("reply-author")[0];
    var timeText = authorText.getElementsByClassName("reply-time")[0];
    var timeString = (new Date()).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
    authorText.innerHTML = "You<span class='reply-time'>" + timeString + "</span>";

    var replyText = replyDivClone.getElementsByClassName("reply-content")[0];
    var replyTextBox = replyDiv.getElementsByClassName("make-reply")[0].getElementsByClassName("reply-form")[0].getElementsByClassName("form-group")[0].getElementsByClassName("form-control")[0];
    
    if(replyTextBox.value != "") {
        replyText.textContent = "" + replyTextBox.value;
        replyTextBox.value = "";

        replyDiv.insertBefore(clone, replyDiv.getElementsByClassName("make-reply")[0]);
        replyDiv.getElementsByClassName("make-reply")[0].style.display = "none";
    }

}