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
write-host "==============================================================================================================="
write-host "`n"
write-host "trying the other meothod to push"
start-sleep -seconds 3
git pull origin main
start-sleep -seconds 5
$git_pull_push=git push origin main
start-sleep -seconds 5
if ($LASTEXITCODE -ne 0){
    write-host "Error occured while git push:`n"
write-host $git_pull_push
}
else{
    write-host "push is Completed successfully"
}
}
else{
write-host "push is successfull"
}
