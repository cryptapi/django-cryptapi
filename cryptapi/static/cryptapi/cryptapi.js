function truncate(text, startChars, endChars, maxLength) {
    if (text.length > maxLength) {
        var start = text.substring(0, startChars);
        var end = text.substring(text.length - endChars, text.length);
        return start + '...' + end;
    }
    return text;
}

function check_status(id) {
    let is_paid = false;

    function status_loop() {
        if (is_paid) return;

        $.getJSON(window.location.protocol + "//" + window.location.host + '/cryptapi/status/?request_id=' + id, function (data) {

            let waiting_payment = jQuery('.waiting_payment');
            let waiting_network = jQuery('.waiting_network');
            let payment_done = jQuery('.payment_done');

            jQuery('.ca_value').html(data.remaining);
            jQuery('.ca_fiat_total').html(data.fiat_remaining);
            jQuery('.ca_copy.ca_details_copy').attr('data-tocopy', data.remaining);

            if (data.data.is_pending === 1) {
                waiting_payment.addClass('done');
                waiting_network.addClass('done');
                jQuery('.ca_loader').remove();
                jQuery('.ca_notification_refresh').remove();
                jQuery('.ca_notification_cancel').remove();

                setTimeout(function () {
                    jQuery('.ca_payments_wrapper').slideUp('400');
                    jQuery('.ca_payment_processing').slideDown('400');
                }, 5000);
            }

            if (data.data.is_paid === 1) {
                waiting_payment.addClass('done');
                waiting_network.addClass('done');
                payment_done.addClass('done');
                jQuery('.ca_loader').remove();
                jQuery('.ca_notification_refresh').remove();
                jQuery('.ca_notification_cancel').remove();

                setTimeout(function () {
                    jQuery('.ca_payments_wrapper').slideUp('400');
                    jQuery('.ca_payment_processing').slideUp('400');
                    jQuery('.ca_payment_confirmed').slideDown('400');
                }, 5000);

                is_paid = true;
            }

            if (data.data.show_min_fee === 1) {
                jQuery('.ca_notification_remaining').show();
            } else {
                jQuery('.ca_notification_remaining').hide();
            }

            if (data.data.remaining !== data.crypto_total) {
                jQuery('.ca_notification_payment_received').show();
                jQuery('.ca_notification_cancel').remove();
                jQuery('.ca_notification_ammount').html(data.already_paid + ' ' + data.coin + ' (<strong>' + data.already_paid_fiat + ' ' + data.fiat_symbol + '<strong>)');
            }

            if (data.payments) {
                let history = data.payments;

                if (jQuery('.ca_history_fill tr').length < Object.entries(history).length + 1) {
                    jQuery('.ca_history').show();

                    jQuery('.ca_history_fill td:not(.ca_history_header)').remove();

                    Object.entries(history).forEach(([key, value]) => {
                        let time = new Date(value.timestamp * 1000).toLocaleTimeString(document.documentElement.lang);
                        let date = new Date(value.timestamp * 1000).toLocaleDateString(document.documentElement.lang);

                        jQuery('.ca_history_fill').append(
                            '<tr>' +
                            '<td>' + value.timestamp + '</td>' +
                            '<td>' + value.value_coin + '</td>' +
                            '</tr>'
                        )
                    });
                }
            }

            if (jQuery('.ca_time_refresh')[0]) {
                var timer = jQuery('.ca_time_seconds_count');

                if (timer.attr('data-seconds') <= 0) {
                    timer.attr('data-seconds', data.counter);
                }
            }
        });

        setTimeout(status_loop, 5000);
    }

    status_loop();
}


function copyToClipboard(text) {
    if (window.clipboardData && window.clipboardData.setData) {
        return clipboardData.setData("Text", text);

    } else if (document.queryCommandSupported && document.queryCommandSupported("copy")) {
        var textarea = document.createElement("textarea");
        textarea.textContent = text;
        textarea.style.position = "fixed";
        document.body.appendChild(textarea);
        textarea.select();
        try {
            return document.execCommand("copy");
        } catch (ex) {
            console.warn("Copy to clipboard failed.", ex);
            return false;
        } finally {
            document.body.removeChild(textarea);
        }
    }
}

$(function () {
    $('.ca_show_qr').on('click', function (e) {
        e.preventDefault();

        let qr_code_close_text = $('.ca_show_qr_close');
        let qr_code_open_text = $('.ca_show_qr_open');

        if ($(this).hasClass('active')) {
            $('.ca_qrcode_wrapper').slideToggle(500);
            $(this).removeClass('active');
            qr_code_close_text.addClass('active');
            qr_code_open_text.removeClass('active');

        } else {
            $('.ca_qrcode_wrapper').slideToggle(500);
            $(this).addClass('active');
            qr_code_close_text.removeClass('active');
            qr_code_open_text.addClass('active');
        }
    });

    $('.ca_copy').on('click', function () {
        copyToClipboard($(this).attr('data-tocopy'));
        let tip = $(this).find('.ca_tooltip.tip');
        let success = $(this).find('.ca_tooltip.success');

        success.show();
        tip.hide();

        setTimeout(function () {
            success.hide();
            tip.show();
        }, 5000);
    })
})
