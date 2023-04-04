<#

.SYNOPSIS
Starts a classic game of Hangman in PowerShell.

.DESCRIPTION
Players discover puzzle words or phrases by suggesting letters.
Each incorrect guess adds an element to the hangman diagram.
The game ends when a solution is guessed, or a diagram is completed.

Various word and phrase dictionaries can be found online.

A dictionary can be a simple list of words or phrases, one per line.
For example:  hangman
              tic-tac-toe
              powershell programming

An optional category can be specified by adding a comma separator.
For example:  classic games, hangman
              classic games, tic-tac-toe
              computers, powershell programming

Please consider giving to cancer research.

.PARAMETER path
Specifies the path to a dictionary file of puzzle words and phrases.

.INPUTS
None.

.OUTPUTS
A whole lot of fun.

.EXAMPLE
.\Start-Hangman.ps1
Starts the program with the default options.

.EXAMPLE
.\Start-Hangman.ps1 -path ".\dictionary.txt"
Starts the program with a custom dictionary of puzzle words and phrases.

.NOTES
MIT License

Copyright (c) 2023 TigerPointe Software, LLC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

If you enjoy this software, please do something kind for free.

History:
01.00 2023-Apr-01 Scott S. Initial release.
01.01 2023-Apr-04 Scott S. Fix whitespace.

.LINK
https://en.wikipedia.org/wiki/Hangman_(game)

.LINK
https://en.wikipedia.org/wiki/ASCII_art

.LINK
https://braintumor.org/

.LINK
https://www.cancer.org/

#>

param
(

  # Defines the default path to a dictionary file of puzzle words and phrases
  # (the default data file must be placed in the same folder as this script)
  [string]$path = ".\hangman.txt"

)

# Gets a new mask value that includes the current guess
function Get-NewMask
{
  param
  (
      [string]$word  # the original word value
    , [string]$mask  # the mask with placeholders
    , [string]$guess # the letter guess
  )

  # Replace matching characters in the mask with the guess value
  # (starts with the puzzle word and copies back the mask characters)
  $chars = $word.ToCharArray();
  for ($i = 0; $i -lt $chars.Length; $i++)
  {
    if ($chars[$i] -ne $guess)
    {
      $chars[$i] = $mask.Substring($i, 1);
    }
  }
  return ($chars -join ""); # returns the updated mask value

}

# Read the entire dictionary file
Write-Host -Object "Loading ...";
Start-Sleep -Milliseconds 500;
$words = (Get-Content -Path $path -ErrorAction Stop);

# Define the list of special non-alphabetic characters
$special = " !`"#$%&'()*+,-./0123456789:;<=>?@[\]^_``{|}~".ToCharArray();

# Define the ASCII art (originally created by Scott S.)
$ascii = @"
  [ ]============[]
  | |/     |
  | |      |
  | |
  | |
  | |
  | |
  | |
  | |
  | |
  | |
  | |
  | |
  | |
  | |
  | |  .=======.
 /   \ |       |
'"'"'"'"'"'"'"'"'"'
  [ ]============[]
  | |/     |
  | |      |
  | |    /////
  | |   {|_ _|}
  | |   O| o |O
  | |    ( - )
  | |     ===
  | |
  | |
  | |
  | |
  | |
  | |
  | |
  | |  .=======.
 /   \ |       |
'"'"'"'"'"'"'"'"'"'
  [ ]============[]
  | |/     |
  | |      |
  | |    /////
  | |   {|. .|}
  | |   O| o |O
  | |    ( O )
  | |   _ === _
  | |  [  \./  ]
  | |    | . |
  | |    |=O=|
  | |    '   '
  | |
  | |
  | |
  | |  .=======.
 /   \ |       |
'"'"'"'"'"'"'"'"'"'
  [ ]============[]
  | |/     |
  | |      |
  | |    /////
  | |   {|. _|}
  | |   O| o |O
  | |    ( - )
  | |   _ === _
  | |  [  \./  ]
  | |  | | . |
  | |  |_|=O=|
  | |  (_'   '
  | |
  | |
  | |
  | |  .=======.
 /   \ |       |
'"'"'"'"'"'"'"'"'"'
  [ ]============[]
  | |/     |
  | |      |
  | |    /////
  | |   {|_ .|}
  | |   O| o |O
  | |    ( - )
  | |   _ === _
  | |  [  \./  ]
  | |  | | . | |
  | |  |_|=O=|_|
  | |  (_'   '_)
  | |
  | |
  | |
  | |  .=======.
 /   \ |       |
'"'"'"'"'"'"'"'"'"'
  [ ]============[]
  | |/     |
  | |      |
  | |    /////
  | |   {|. .|}
  | |   O| o |O
  | |    ( - )
  | |   _ === _
  | |  [  \./  ]
  | |  | | . | |
  | |  |_|=O=|_|
  | |  (_' | '_)
  | |    | |
  | |   .|_|
  | |  (___'
  | |  .=======.
 /   \ |       |
'"'"'"'"'"'"'"'"'"'
  [ ]============[]
  | |/     |
  | |      |
  | |    /////
  | |   {|. .|}
  | |   O| o |O
  | |    ( O )
  | |   _ === _
  | |  [  \./  ]
  | |  | | . | |
  | |  |_|=O=|_|
  | |  (_' | '_)
  | |    | | |
  | |   .|_|_|.
  | |  (___'___)
  | |  .=======.
 /   \ |       |
'"'"'"'"'"'"'"'"'"'
  [ ]============[]
  | |/     |
  | |      |
  | |      |
  | |    /////
  | |   {|x x|}
  | |   O| o |O
  | |    (---)
  | |   _ === _
  | |  [  \./  ]
  | |  | | . | |
  | |  |_|=O=|_|
  | |  (_' | '_)
  | |    | | |
  | |   .|_|_|.
  | |  (___'___)
 /   \
'"'"'"'"'"'"'"'"'"'
  [ ]============[]
  | |/
  | |
  | |   Yippee!
  | |
  | |    /////
  | |   {|. .|}
  | |   O| o |O
  | |    ( ~ )
  | |   _.| |._
  | |  [  \./  ]
  | |  | | . | |
  | |  |_|=O=|_|
  | |  (_' | '_)
  | |    | | |
  | |   .|_|_|.
 /   \ (___'___)
'"'"'"'"'"'"'"'"'"'
"@;

# Use a try-catch for exceptions because the host is cleared on each guess
# (otherwise, the exception messages get cleared with the console)
try
{

  # Define the ASCII art panel variables
  $height = 18;                       # number of text lines per panel
  $width  = 22;                       # includes the horizontal padding
  $ascii  = $ascii.Replace("`r", ""); # removes the carriage returns
  $lines  = $ascii.Split("`n");       # splits on the line feeds

  # Loop while more games are selected
  $more = "Y";
  while ($more -eq "Y")
  {

    # Initialize the loop control variables
    $solved  = $false; # not solved
    $count   = 0;      # no guesses
    $maximum = 8;      # wrong guesses, number of ASCII art panels minus one

    # Initialize the puzzle variables (includes an optional category)
    $remain   = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; # holds the remaining letters
    $category = "";
    $word     = (Get-Random -InputObject $words).Trim().ToUpper();
    $idx      = $word.LastIndexOf(","); # finds optional category separator
    if ($idx -ge 0)
    {
      $category = "The category is $($word.Substring(0, $idx).Trim())";
      $idx++;
      $word     = $word.Substring($idx, ($word.Length - $idx)).Trim();
    }

    # Create a mask and replace the special characters to support phrases
    $mask = ("." * $word.Length); # repeats a placeholder for each character
    foreach ($chr in $special)
    {
      $mask = (Get-NewMask -word $word -mask $mask -guess $chr);
    }

    # Loop while not solved and remaining guesses are available
    while ((-not $solved) -and ($count -lt $maximum))
    {

      # Check for a solved puzzle and skip to the winning count value
      if ($mask -eq $word)
      {
        $solved = $true;
        $count  = $maximum;
      }

      # Display the ASCII art panel for the current count value
      Clear-Host;
      Write-Host;
      for ($i = 0; $i -lt $height; $i++)
      {
        $line = $lines[($count * $height) + $i];
        $line = $line.PadRight($width);
        if ($i -eq  3) { $line = "$line Welcome to HANGMAN"; }
        if ($i -eq  4) { $line = "$line $category"; }
        if ($i -eq  7) { $line = "$line $mask";     }
        if ($i -eq 11) { $line = "$line Remaining Letters:"; }
        if ($i -eq 12) { $line = "$line $remain";   }
        Write-Host $line;
      }

      # If solved, exit the loop (winning screen has been drawn)
      if ($solved) { continue; }

      # Otherwise, check for remaining guesses
      if ($count -lt ($maximum - 1))
      {

        # Read the next guess (limited to the remaining letters only)
        $guess = "";
        while (($guess.Length -ne 1) -or (-not $remain.Contains($guess)))
        {
          $guess = Read-Host -Prompt `
                     "Please choose one of the remaining letters";
          $guess = $guess.ToUpper();
        }
        $remain = $remain.Replace($guess, " ");

        # Check for a correct guess and update the mask
        if (($guess -ne " ") -and ($word.Contains($guess)))
        {
          $mask = (Get-NewMask -word $word -mask $mask -guess $guess);
          continue;
        }

      }
      $count++;

    } # end solved-count-maximum loop

    # Display the solution message
    $message = "GACK!";
    if ($solved) { $message = "Congratulations!"; }
    Write-Host "$message  The solution was $word.";

    # Prompt for another game
    $more = "";
    while (($more.Length -ne 1) -or (-not ("YN").Contains($more)))
    {
      $more = Read-Host -Prompt "Do you want to play another game? (Y/N)";
      $more = $more.ToUpper();
    }

  } # end more loop

}
catch
{
  Write-Error $_;
}