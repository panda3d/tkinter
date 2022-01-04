#platform=manylinux2014_x86_64
#abis="cp36-cp36m cp37-cp37m cp38-cp38 cp39-cp39 cp310-cp310"

platform=manylinux2010_x86_64
abis="cp36-cp36m cp37-cp37m cp38-cp38 cp39-cp39 cp310-cp310"

#platform=manylinux1_x86_64
#abis="cp36-cp36m cp37-cp37m cp38-cp38 cp39-cp39"

dockerfile=$(mktemp)

cat << EOF > $dockerfile
FROM quay.io/pypa/$platform
RUN yum -y install tk
ADD . /work
EOF

cat $dockerfile

docker build -t ${platform}_tk -f $dockerfile .

for abi in $abis; do
  docker run --rm -v `pwd`/dist:/dist -w /work ${platform}_tk bash -c "/opt/python/$abi/bin/python setup.py bdist_wheel && auditwheel repair -L /../_tkinter_ext -w /dist/ dist/*.whl"
done
