<#
Merge-And-Clean-TextFiles.ps1

```
Purpose:
- Merge a large number of text files into a single output file.
- Remove lines containing a specific keyword.
- Remove empty lines.
- Optionally remove a prefix from the beginning of a line.
- Display progress while processing.

Typical use cases:
- Cleaning log files
- Merging scraped text data
- Preparing data for PostgreSQL imports
- Removing metadata lines from text collections

Usage:
1. Edit the configuration section below.
2. Save the script.
3. Run from PowerShell:

   .\Merge-And-Clean-TextFiles.ps1
```

#>

# --------------------------------------------------

# Configuration

# --------------------------------------------------

# Folder containing the source text files

$SourceFolder = "WRITE-YOUR-SOURCE-PATH-HERE"

# Output file to create

$OutputFile = "WRITE-YOUR-OUTPUT-FILE-PATH-HERE"

# Remove any line containing this keyword

# Example:

# "Password:"

# "DEBUG"

# "ERROR"

$KeywordToDeleteWholeLine = "WRITE-YOUR-KEYWORD-HERE-TO-DELETE-WHOLE-LINE"

# Remove this text from the beginning of a line

# Example:

# "addr: "

# "address: "

#

# Leave empty ("") if not needed.

$TextToRemoveFromLineStart = "WRITE-YOUR-KEYWORD-HERE-OR-LEAVE-EMPTY-IF-NOT-NEEDED"

# Show progress every N files

$ProgressInterval = 1000

# --------------------------------------------------

# Script

# --------------------------------------------------

Write-Host "Starting..."
Write-Host "Source: $SourceFolder"
Write-Host "Output: $OutputFile"

$Writer = New-Object System.IO.StreamWriter($OutputFile, $false)

$FileCount = 0
$LineCount = 0

Get-ChildItem $SourceFolder -Filter *.txt | ForEach-Object {

```
$FileCount++

if (($FileCount % $ProgressInterval) -eq 0) {
    Write-Host "Processed $FileCount files..."
}

foreach ($Line in Get-Content $_.FullName) {

    $Line = $Line.Trim()

    # Skip empty lines
    if ($Line.Length -eq 0) {
        continue
    }

    # Skip lines containing the keyword
    if (
        $KeywordToDeleteWholeLine -ne "" -and
        $Line -match [regex]::Escape($KeywordToDeleteWholeLine)
    ) {
        continue
    }

    # Remove prefix from line start if configured
    if ($TextToRemoveFromLineStart -ne "") {

        $Pattern = '^' + [regex]::Escape($TextToRemoveFromLineStart)

        $Line = $Line -replace $Pattern, ''
    }

    $Writer.WriteLine($Line)

    $LineCount++
}
```

}

$Writer.Close()

Write-Host ""
Write-Host "Finished."
Write-Host "Files processed : $FileCount"
Write-Host "Lines written   : $LineCount"
Write-Host "Output file     : $OutputFile"
