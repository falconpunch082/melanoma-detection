let totalPoints = 0;

function startQuestionnaire() {
    var questionair = document.getElementById('questionContainer');

    // Perform an AJAX request to fetch the story.html content
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/static/contents/questionnaire.html', true); // path to the story

    xhr.onload = function () {
        if (xhr.status === 200) {
            // Insert the fetched content into the story container
            questionair.innerHTML = xhr.responseText;
            console.error('loaded questionair.html');
            document.getElementById('question1').style.display = 'block';
            document.getElementById('questionButton').style.display = 'none';
        } else {
            console.error('Failed to fetch questionair.html');
        }
    };

    xhr.onerror = function () {
        console.error('Failed to fetch questionair.html');
    };

    xhr.send();
    
}
    function nextQuestion(questionNumber) {
        let questionId = 'question' + questionNumber;
        let nextQuestionId = 'question' + (questionNumber + 1);
        let selectedValue = document.querySelector('input[name="q' + questionNumber + '"]:checked');

        if (selectedValue) {
            totalPoints += parseInt(selectedValue.value);
            document.getElementById(questionId).style.display = 'none';
            if (document.getElementById(nextQuestionId)) {
                document.getElementById(nextQuestionId).style.display = 'block';
            } else {
                calculateResult();
            }
        } else {
            alert('Please select an answer.');
        }
    }

    function calculateResult() {
        let resultText = '';
        let submitButton=document.getElementById('submitQuestion')

            // Check if the button text is 'Submit'
        if (submitButton.textContent.trim().toLowerCase() === 'submit') {
            // Change button text to 'Re-Submit'
            submitButton.textContent = 'Re-Submit'
            if (totalPoints <= 5) {
                resultText = "Your point: "+ totalPoints +".<br><span style=\"color:coral;\">Description:</span> Based on your responses, there is a low likelihood of potential cancer presence. However, it's important to note that this assessment is preliminary. If you have any concerns or uncertainties, we recommend seeking medical advice for a thorough evaluation.";
            } else {
                resultText = "Your point: "+ totalPoints +".<br><span style=\"color:coral;\">Description:</span> Your responses indicate a possibility of elevated risk for potential cancer presence. To better assess and provide accurate insights, we kindly request you to upload an image of the skin lesion or mole for further detailed analysis by our model.";
            }
            document.getElementById('resultText').innerHTML = resultText;
            document.getElementById('result').style.display = 'block';
        } else {
            // Reload the webpage
            location.reload();
        }
    }
    
    