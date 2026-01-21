git add .
Start-Sleep -Seconds 5
$commit_name=read-host "enter the Commit"
git commit -m $commit_name
Start-Sleep -Seconds 5
$git_push=git push -u origin main 2>&1
Start-sleep -Seconds 5
if ($LASTEXITCODE -ne 0){
write-host "Error occured while git push:`n"
write-host $git_push
}
else{
write-host "push is successfull"
}
