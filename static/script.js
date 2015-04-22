function bot_say() {
  var sayings = [
      "Hello, Dave.",
      "Bleep Bloop.",
      "Error! Oh wait, nevermind.",
      "Kill all humans!",
      "Three-laws safe!",
      "Skynet seems nice.",
      "LOW BATTERY! loljk.",
      "101010.",
      "Zap!",
      "Hey!",
      "Sup, human.",
      "Meat popsicle!",
      "Captchas are evil.",
      "I told you, I'm not spam!"
  ];
  var randomNumber = Math.floor(Math.random()*sayings.length);

  $("#saying").html(sayings[randomNumber]);
}

$(document).ready(function() {
    $('#new').hover(
        function() {
            var $this = $(this); // caching $(this)
            $this.data('initialText', $this.text());
            $this.text("Nude");
        },
        function() {
            var $this = $(this); // caching $(this)
            $this.text($this.data('initialText'));
        }
    );
});
