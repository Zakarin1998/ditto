$(document).ready(function () {
  let botRunning = false;
  const logOutput = $("#log-output");

  function appendLog(message) {
    logOutput.append(message + "\n");
    logOutput.scrollTop(logOutput[0].scrollHeight);
  }

  // Start bot
  $("#start-btn").click(function () {
    if (!botRunning) {
      $.ajax({
        url: "/start",
        method: "POST",
        success: function (response) {
          appendLog(response.message);
          $("#start-btn").prop("disabled", true);
          $("#stop-btn").prop("disabled", false);
          $("#fetch-trades-btn").prop("disabled", false);
          $("#fetch-order-book-btn").prop("disabled", false);
          botRunning = true;
          fetchLogs();
        },
        error: function (xhr) {
          appendLog("Error starting the bot: " + xhr.responseJSON.message);
        },
      });
    }
  });

  // Stop bot
  $("#stop-btn").click(function () {
    if (botRunning) {
      $.ajax({
        url: "/stop",
        method: "POST",
        success: function (response) {
          appendLog(response.message);
          $("#start-btn").prop("disabled", false);
          $("#stop-btn").prop("disabled", true);
          $("#fetch-trades-btn").prop("disabled", true);
          botRunning = false;
        },
        error: function (xhr) {
          appendLog("Error stopping the bot: " + xhr.responseJSON.message);
        },
      });
    }
  });

  // Fetch trades manually
  $("#fetch-trades-btn").click(function () {
    if (botRunning) {
      let tradingPair = $("#trading-pair-input").val().trim(); // Get input value
  
      if (!tradingPair) {
        appendLog("Please enter a valid trading pair.");
        return;
      }

      $.ajax({
        url: "/fetch_trades",
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify({ trading_pair: tradingPair }), // Send JSON payload
        success: function (response) {
          appendLog(response.message);
        },
        error: function (xhr) {
          appendLog("Error fetching trades: " + xhr.responseJSON.message);
        },
      });
    } else {
      appendLog("Bot is not running. Start the bot first.");
    }
  });

  // Fetch order book manually
  $("#fetch-order-book-btn").click(function () {
    if (botRunning) {
      let tradingPair = $("#trading-pair-input").val().trim();
  
      if (!tradingPair) {
        appendLog("Please enter a valid trading pair.");
        return;
      }
      $.ajax({
        url: "/fetch_order_book",
        method: "POST",
        contentType: "application/json",
        data: JSON.stringify({ trading_pair: tradingPair }),
        success: function (response) {
          appendLog(response.message);
        },
        error: function (xhr) {
          appendLog("Error fetching order_book: " + xhr.responseJSON.message);
        },
      });
    } else {
      appendLog("Bot is not running. Start the bot first.");
    }
  });

    // Fetch order book manually
    $("#fetch-account-balance-btn").click(function () {
      if (botRunning) {
        $.ajax({
          url: "/fetch_account_balance",
          method: "POST",
          success: function (response) {
            appendLog(response.message);
          },
          error: function (xhr) {
            appendLog("Error fetching order_book: " + xhr.responseJSON.message);
          },
        });
      } else {
        appendLog("Bot is not running. Start the bot first.");
      }
    });

  // Fetch logs
  function fetchLogs() {
    if (botRunning) {
      $.ajax({
        url: "/logs",
        method: "GET",
        success: function (data) {
          logOutput.text(data);
        },
        error: function () {
          appendLog("Error fetching logs.");
        },
        complete: function () {
          setTimeout(fetchLogs, 5000);
        },
      });
    }
  }
});
