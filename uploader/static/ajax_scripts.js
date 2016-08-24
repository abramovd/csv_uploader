//configuration
var max_file_size 			= 20485760; //allowed file size. (1 MB = 1048576)
var allowed_file_types 		= ['image/png', 'image/gif', 'image/jpeg', 'image/pjpeg', 'csv']; //allowed file types
var result_output 			= '#output'; //ID of an element for response output
var my_form_id 				= '#upload_form'; //ID of an element for response output
var progress_bar_id 		= '#progress-wrp'; //ID of an element for response output
var total_files_allowed 	= 3; //Number files allowed to upload



//on form submit
$(my_form_id).on( "submit", function(event) {
    event.preventDefault();
    var proceed = true; //set proceed flag
    var error = [];	//errors
    var total_files_size = 0;

    //reset progressbar
    $(progress_bar_id + " .progress-bar").css("width", "0%");
    $(progress_bar_id + " .status").text("0%");

    if (!window.File && window.FileReader && window.FileList && window.Blob) { //if browser doesn't supports File API
        error.push("Your browser does not support new File API! Please upgrade."); //push error text
    } else {
        var total_selected_files = this.elements['file'].files.length; //number of files

        //limit number of files allowed
        if (total_selected_files > total_files_allowed) {
            error.push("You have selected " + total_selected_files + " file(s), " + total_files_allowed + " is maximum!"); //push error text
            proceed = false; //set proceed flag to false
        }
        //iterate files in file input field
        $(this.elements['file'].files).each(function (i, ifile) {
            if (ifile.value !== "") { //continue only if file(s) are selected

                total_files_size = total_files_size + ifile.size; //add file size to total size
            }
        });

        //if total file size is greater than max file size
        if (total_files_size > max_file_size) {
            error.push("You have " + total_selected_files + " file(s) with total size " + total_files_size + ", Allowed size is " + max_file_size + ", Try smaller file!"); //push error text
            proceed = false; //set proceed flag to false
        }

        var submit_btn = $(this).find("input[type=submit]"); //form submit button

        //if everything looks good, proceed with jQuery Ajax
        if (proceed) {
            //submit_btn.val("Please Wait...").prop( "disabled", true); //disable submit button
            var form_data = new FormData(this); //Creates new FormData object
            var post_url = $(this).attr("action"); //get action URL of form

            //jQuery Ajax to Post form data
            $.ajax({
                url: post_url,
                type: "POST",
                data: form_data,
                contentType: false,
                cache: false,
                processData: false,
                xhr: function () {
                    //upload Progress
                    var xhr = $.ajaxSettings.xhr();
                    if (xhr.upload) {
                        xhr.upload.addEventListener('progress', function (event) {
                            var percent = 0;
                            var position = event.loaded || event.position;
                            var total = event.total;
                            if (event.lengthComputable) {
                                percent = Math.ceil(position / total * 100);
                            }
                            //update progressbar
                            $(progress_bar_id + " .progress-bar").css("width", +percent + "%");
                            $(progress_bar_id + " .status").text(percent + "%");
                        }, true);
                    }
                    return xhr;
                },
                mimeType: "multipart/form-data",
                success: function (res) { //
                    $(my_form_id)[0].reset(); //reset form
                    $(result_output).html("Successfully uploaded!"); //output response from server
                    submit_btn.val("Upload").prop("disabled", false); //enable submit button once ajax is done
                },
                error: function (res) {
                    $(result_output).html(res.responseText); //reset output
                }

            });
        }
    }
});


        function start_parser() {
            // add task status elements
            div = $('<div class="progress"><div></div><div>0%</div><div>...</div><div>&nbsp;</div></div><hr>');
            $('#progress').append(div);

            // create a progress bar
            var nanobar = new Nanobar({
                bg: '#44f',
                target: div[0].childNodes[0]
            });

            // send ajax POST request to start background job
            $.ajax({
                type: 'POST',
                url: '/parser',
                xhr: function() {
                        var myXhr = $.ajaxSettings.xhr();
                        if(myXhr.upload){
                            myXhr.upload.addEventListener('progress', progress, false);
                        }
                        return myXhr;
                },
                cache:false,
                contentType: false,
                processData: false,

                success: function(data, status, request) {
                    status_url = request.getResponseHeader('Location');
                    update_progress(status_url, nanobar, div[0]);
                },
                error: function(res) {
                    alert('Cannot process CSV')
                }
            });
        }
        function update_progress(status_url, nanobar, status_div) {
            // send GET request to status URL
            $.getJSON(status_url, function(data) {
                // update UI
                percent = parseInt(data['current'] * 100 / data['total']);
                nanobar.go(percent);
                $(status_div.childNodes[1]).text(percent + '%');
                $(status_div.childNodes[2]).text(data['status']);
                if (data['state'] != 'PENDING' && data['state'] != 'PROGRESS') {
                    if ('result' in data) {
                        // show result
                        $(status_div.childNodes[3]).text('Result: ' + data['result']);
                    }
                    else {
                        // something unexpected happened
                        $(status_div.childNodes[3]).text('Result: ' + data['state']);
                    }
                }
                else {
                    // rerun in 1 seconds
                    setTimeout(function() {
                        update_progress(status_url, nanobar, status_div);
                    }, 1000);
                }
            });
        }
       $(function() {
            $('#start-bg-job').click(start_parser);
        });

    $(document).ready(function(){
    $.ajax({ url: "get_tasks",
            context: document.body,
            success:
                    function(data, status, request) {
                        status_url = request.getResponseHeader('Task');
                        if (status_url) {
                            div = $('<div class="progress"><div></div><div>0%</div><div>...</div><div>&nbsp;</div></div><hr>');
                $('#progress').append(div);

                // create a progress bar
                var nanobar = new Nanobar({
                    bg: '#44f',
                    target: div[0].childNodes[0]
                });
                            update_progress(status_url, nanobar, div[0]);
                        }
                    },
            error: function (res) {
                $(result_output).html("No current tasks"); //reset output
            }
    })});