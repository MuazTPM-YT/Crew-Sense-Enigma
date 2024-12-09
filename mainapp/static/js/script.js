function openTab(event, tabName) {
    $('.tab-content').hide(); 
    $('.tab-link').removeClass('active'); 

    $(`#${tabName}`).show(); 
    $(event.target).addClass('active'); 
}

$(document).ready(function () {
    let inputText = ''; 
    let outputText = ''; 
    let mode = "text_to_braille"; 

    $('#left-english-btn').click(function () {
        $(this).addClass('selected');
        $('#left-braille-btn').removeClass('selected');
        $('#right-braille-btn').addClass('selected');
        $('#right-english-btn').removeClass('selected');
        
        inputText = $('.text-input').val();
        outputText = $('.text-output').val();

        $('.text-input').val(outputText);
        $('.text-output').val(inputText);

        mode = "text_to_braille"; 
        $('.text-input').attr("placeholder", "Type English here...");
        $('.text-output').attr("placeholder", "Braille output...");
    });

    $('#left-braille-btn').click(function () {
        $(this).addClass('selected');
        $('#left-english-btn').removeClass('selected');
        $('#right-english-btn').addClass('selected');
        $('#right-braille-btn').removeClass('selected');

        inputText = $('.text-input').val();
        outputText = $('.text-output').val();

        $('.text-input').val(outputText);
        $('.text-output').val(inputText);

        mode = "braille_to_text"; 
        $('.text-input').attr("placeholder", "Type Braille here...");
        $('.text-output').attr("placeholder", "Text output...");
    });

    $('.text-input').on('input', function () {
        const textInput = $(this).val();

        $.ajax({
            url: '/convert-text-to-braille/',
            type: 'POST',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}',
            },
            data: JSON.stringify({ text: textInput, mode: mode }),
            contentType: 'application/json',
            success: function (response) {
                $('.text-output').val(response.output);
            },
            error: function (error) {
                console.error('Error:', error);
            },
        });
    });
});

  document.getElementById("copyButton").addEventListener("click", function () {
    const icon = document.getElementById("iconImage");
    const originalSrc = icon.src;
    const textareaContent = document.querySelector(".text-output").value; 

    navigator.clipboard.writeText(textareaContent).then(() => {
        console.log("Copied to clipboard!");

        icon.classList.add("hidden");

        setTimeout(function () {
            icon.src = staticCheckUrl;
            icon.classList.remove("hidden");
        }, 100);

        setTimeout(function () {
            icon.classList.add("hidden");
            setTimeout(function () {
                icon.src = originalSrc;
                icon.classList.remove("hidden");
            }, 100);
        }, 1500);
    }).catch(err => {
        console.error("Failed to copy text: ", err);
    });
});

$(document).ready(function () {
    // File input change handler for documents
    $('#fileInput').change(function () {
        const fileInput = $(this)[0].files[0];
        if (!fileInput) {
            alert("No file selected.");
            return;
        }

        const formData = new FormData();
        formData.append('file', fileInput);
        formData.append('csrfmiddlewaretoken', csrfToken); // CSRF token for Django

        // Show a loading indicator in the output box
        $('.content-box-right .text-output').val("Processing file...");

        // Step 1: Upload the file and extract its content
        $.ajax({
            url: '/upload-file/', // Backend endpoint for file content extraction
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                if (response.translation) {
                    const englishText = response.translation;

                    // Show the extracted English text in the left content box
                    $('.content-box-left .text-input').val(englishText);

                    // Step 2: Translate English text to Braille
                    translateTextToBraille(englishText);
                } else {
                    alert("File processing failed. No text extracted.");
                    $('.content-box-right .text-output').val("");
                }
            },
            error: function (xhr, status, error) {
                alert("An error occurred while processing the file.");
                console.error("File Processing Error:", xhr.responseText || error);
                $('.content-box-right .text-output').val("File processing error.");
            },
        });
    });

    // File input change handler for images
    $('#imageInput').change(function () {
        const fileInput = $(this)[0].files[0];
        if (!fileInput) {
            alert("No image selected.");
            return;
        }

        const formData = new FormData();
        formData.append('file', fileInput);
        formData.append('csrfmiddlewaretoken', csrfToken);

        // Show a loading indicator
        $('.content-box-right .text-output').val("Processing image...");

        // Step 1: Extract text from the image
        $.ajax({
            url: '/upload-image/', // Backend endpoint for extracting text
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                if (response.file_content) {
                    const extractedText = response.file_content;

                    // Show the extracted text in the left content box
                    $('.content-box-left .text-input').val(extractedText);

                    // Step 2: Translate extracted text to Braille
                    translateTextToBraille(extractedText);
                } else {
                    alert("No text content extracted from the image.");
                    $('.content-box-right .text-output').val("");
                }
            },
            error: function (xhr, status, error) {
                alert("An error occurred while processing the image.");
                console.error("Image Processing Error:", xhr.responseText || error);
                $('.content-box-right .text-output').val("Image processing error.");
            },
        });
    });

    // Function to translate text to Braille
    function translateTextToBraille(text) {
        $('.content-box-right .text-output').val("Translating to Braille...");
        $.ajax({
            url: '/convert-text-to-braille/', // Backend endpoint for Braille translation
            type: 'POST',
            headers: {
                'X-CSRFToken': csrfToken, // CSRF token for Django
            },
            data: JSON.stringify({ text: text, mode: "text_to_braille" }),
            contentType: 'application/json',
            success: function (response) {
                if (response.output) {
                    // Show Braille translation in the right content box
                    $('.content-box-right .text-output').val(response.output);
                } else {
                    alert("Failed to translate text to Braille.");
                    $('.content-box-right .text-output').val("");
                }
            },
            error: function (xhr, status, error) {
                alert("An error occurred while translating text to Braille.");
                console.error("Braille Translation Error:", xhr.responseText || error);
                $('.content-box-right .text-output').val("Translation error.");
            },
        });
    }
});

$(document).ready(function () {
    $('.listen-button').on('click', function () {
      const text = $('.content-box-left .text-input').val(); 

      if (text) {
        try {
          const speech = new SpeechSynthesisUtterance(text);
          window.speechSynthesis.speak(speech);
        } catch (e) {
          console.error("Error speaking text:", e);
        }
      } else {
        alert("Please enter some text to speak!");
      }
    });
  });

  $(document).ready(function () {
    $('.print-button').on('click', function () {
      const translationContent = $('.content-box-right .text-output').val();
  
      if ($.trim(translationContent)) {
        const printWindow = window.open('', '_blank', 'width=800,height=600');
        printWindow.document.write(`
          <html>
            <head>
              <title>Print Translation</title>
              <style>
                body { font-family: Arial, sans-serif; padding: 20px; }
              </style>
            </head>
            <body>
              ${translationContent}
            </body>
          </html>
        `);
        printWindow.document.close();
        printWindow.focus();
        printWindow.print();
        printWindow.close();
      } else {
        alert("There is no content to print!");
      }
    });
  });

  $(document).ready(function () {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (SpeechRecognition) {
        const recognition = new SpeechRecognition();
        const $textInput = $('.content-box-left .text-input');
        const $textOutput = $('.content-box-right .text-output');
        const $starttext = 'Recording Started';
        const $stoptext = 'Recording Stopped';

        recognition.continuous = true; // Keep listening until stopped
        recognition.interimResults = true; // Show partial results
        recognition.lang = 'en-US'; // Set language to English

        // Start recognition
        function startRecognition() {
            recognition.start();
            console.log('Speech recognition started.');
        }

        // Stop recognition
        function stopRecognition() {
            recognition.stop();
            console.log('Speech recognition stopped.');
        }

        // Translate text to Braille
        function translateTextToBraille(text) {
            $.ajax({
                url: '/convert-text-to-braille/',
                type: 'POST',
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}', // Adjust according to your setup
                },
                data: JSON.stringify({ text: text, mode: 'text_to_braille' }),
                contentType: 'application/json',
                success: function (response) {
                    $textOutput.val(response.output);
                },
                error: function (error) {
                    console.error('Error translating text to Braille:', error);
                    $textOutput.val('Error translating text.');
                },
            });
        }

        // Process speech results
        function printOutput() {
            const outputContent = $textOutput.val();
            if ($.trim(outputContent)) {
                const printWindow = window.open('', '_blank', 'width=800,height=600');
                printWindow.document.write(`
                    <html>
                        <head>
                            <title>Print Output</title>
                        </head>
                        <body>
                            <pre>${outputContent}</pre>
                        </body>
                    </html>
                `);
                printWindow.document.close();
                printWindow.print();
                printWindow.close();
            } else {
                alert('No output available to print.');
            }
        }

        // Process speech results
        recognition.onresult = function (event) {
            const transcript = event.results[event.results.length - 1][0].transcript.trim().toLowerCase();
            console.log(`Recognized: ${transcript}`);

            if (transcript.startsWith('translate')) {
                const textToTranslate = transcript.replace('translate', '').trim();
                $textInput.val(textToTranslate);
                translateTextToBraille(textToTranslate);

            } 
            
            else if (transcript === 'speak') {
                const sstext = $textInput.val();
                if ($textInput) {
                    try {
                      const speech = new SpeechSynthesisUtterance(sstext);
                      window.speechSynthesis.speak(speech);
                    } catch (e) {
                      console.error("Error speaking text:", e);
                    }
                  } else {
                    alert("Please enter some text to speak!");
                  }
            }

            else if (transcript === 'copy') {
                const textToCopy = $textOutput.val().trim(); // Get the text from the right content box
                if (textToCopy) {
                    navigator.clipboard.writeText(textToCopy)
                        .then(() => {
                            console.log('Text copied to clipboard:', textToCopy);
                            alert('Text copied to clipboard!');
                        })
                        .catch(err => {
                            console.error('Failed to copy text:', err);
                            alert('Failed to copy text. Please try again.');
                        });
                } else {
                    console.log('No text to copy.');
                    alert('The right content box is empty. Nothing to copy.');
                }
            }

            else if (transcript === 'print') {
                printOutput();
            } 
            
            else if (transcript === 'clear') {
                $textInput.val('');
                $textOutput.val('');
                translateTextToBraille(textToTranslate);

            } 
            
            else {
                console.log('No matching command recognized.');
            }
        };

        // Handle errors
        recognition.onerror = function (event) {
            console.error(`Speech recognition error: ${event.error}`);
        };

        // Handle recognition end
        recognition.onend = function () {
            console.log('Speech recognition ended.');
        };

        // Keydown event listener for Shift + F and Shift + J
        $(document).on('keydown', function (event) {
            if (event.shiftKey && event.key.toLowerCase() === 'f') {
                event.preventDefault(); // Prevent default behavior for this key combination
                startRecognition();
                const speech = new SpeechSynthesisUtterance($starttext);
                window.speechSynthesis.speak(speech);
            } else if (event.shiftKey && event.key.toLowerCase() === 'j') {
                event.preventDefault(); // Prevent default behavior for this key combination
                stopRecognition();
                const speech = new SpeechSynthesisUtterance($stoptext);
                window.speechSynthesis.speak(speech);
            }
        });
    } else {
        alert('Sorry, your browser does not support speech recognition.');
    }
});

