  #!/bin/bash
  for i in `seq 1 10`;do
    echo item: $i
    echo 'sample $i' >> horner.py
    git add horner.py
    git commit -m 'some random stuff $i time'
    git push
  done