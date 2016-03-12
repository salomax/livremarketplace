/******************************************************************************
 * postal.js
 *
 * Copyright 2016 Marcos Salomão
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * 
 *     http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * @version     1.0
 * @author      Marcos Salomão (salomao.marcos@gmail.com)
 *****************************************************************************/

! function($) {

    $.postal = {};

    $.postal.api = {

        SERVICE_NAME: 'postal',
        VERSION: 'v1',

        service: function(method) {
            return ['/', $.postal.api.SERVICE_NAME, '/', $.postal.api.VERSION, '/', method].join('');
        },

        /* 
         * Get package traking code.
         */
        getTrackingInfo: function(postalService, trackCode) {

            // Execute getTrackingInfo endpoint 
            return $.api.request({
                path: $.postal.api.service([postalService, '/', trackCode].join('')),
                method: 'GET',
                dialogError: {
                    title: messages.postal.trackinginfo.dialog.title,
                    message: messages.postal.trackinginfo.dialog.errormessage
                }
            });

        }, // End getTrackingInfo()

    }; // End $.postal.api

    /**
     * Bind link to tracking info.
     */
    $.fn.bindTrackCode = function() {

        // Get track code by tag attribute
        this.each(function(index, element) {

            var _this = $(element);
            var trackCode = _this.attr('data-trackcode');

            // Not apply plugin if there is not a track code
            if (!trackCode) return;

            // Create button
            var button = $('<button class="btn btn-link btn-sm trakinginfo"><i class="ion ion-android-search"></i></button>');
            button.attr('data-trackcode', trackCode);
            button.bind('click', function() {

                // TODO create other postal services
                var postal_service = 'correios';
                var trackCode = $(this).attr('data-trackcode');

                // Show message
                $(this).after($(['<span class="label label-primary">', messages.postal.trackinginfo.searchingalert, '</span>'].join('')));
                var _button = $(this);

                // Execute endpoint
                $.postal.api.getTrackingInfo(postal_service, trackCode).then(function(response) {

                    // Create table with the info
                    var info = $('<ul class="timeline">');
                    $.each(response.result.items, function(index, item) {

                        info.append((row = $('<li class="time-label">')));
                        $('<span class="bg-green">').text(item.date).appendTo(row);

                        info.append((row = $('<li>')));
                        $('<i class="fa fa-envelope bg-blue">').appendTo(row);

                        row.append((row = $('<div class="timeline-item">')));
                        $('<span class="tracking-info-date">').text(item.status).appendTo(row);
                        row.append((body = $('<div class="timeline-body">')));
                        $('<span class="tracking-status-date">').text(item.local).appendTo(body);
                        $('<span class="tracking-details-date">').text(item.details).appendTo(body);

                    });
                    var content = $('<div>').append(info);

                    // Show modal with the tracking info
                    $('.modal-dialog-message').modalDialog({
                        title: [messages.postal.trackinginfo.dialog.title, trackCode].join(' '),
                        message: content
                    }).default();

                    _button.nextAll().remove();

                });
            }); // End click bind

            // Remove if exists one
            _this.next('button.trakinginfo').remove();

            // Insert
            _this.after(button);

        });


    }; // End $.fn.bindTrackCode

}(jQuery);
