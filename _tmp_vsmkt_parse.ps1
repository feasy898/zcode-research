$r = Get-Content 'D:\workspace\zcode研究\_tmp_vsmkt_resp.json' -Raw | ConvertFrom-Json
$r.results[0].extensions | ForEach-Object {
  $inst = ($_.statistics | Where-Object { $_.statisticName -eq 'install' } | Select-Object -First 1).value
  $rate = ($_.statistics | Where-Object { $_.statisticName -eq 'averagerating' } | Select-Object -First 1).value
  "{0} | publisher={1} | installs={2} | rating={3}" -f $_.displayName, $_.publisher.publisherName, $inst, $rate
}
