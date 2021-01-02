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