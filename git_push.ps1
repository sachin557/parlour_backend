git add .
Start-Sleep -Seconds 5
$commit_name=read-host "enter the Commit"
git commit -m $commit_name
Start-Sleep -Seconds 5
$git_push= git push -u origin main
Start-sleep -Seconds 5
if ($git_push -contains "error"){
write-host "Error occured while git push:`n"
write-host $git_push
}
else{
write-host "push is successfull"
}
