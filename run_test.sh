#!/bin/sh

keyfile='key_v1.txt';
keysize=16;

echo Generating the Key File $keyfile for FHEv1
./FHEv1 -k $keysize $keyfile
echo Key File $keyfile generated!!!
echo

echo Testing the correctness of encryption and decryption
cipher17=$(./FHEv1 -e 17 $keyfile)
plain17=$(./FHEv1 -d $cipher17 $keyfile)
if [ $plain17 -eq 17 ]; then
   echo The encryption and decryption work correctly!!!
   echo
fi

echo Testing homomorphic addition
cipher_sum=$(./FHEv1 -a $cipher17 -e 18 $keyfile)
plain_sum=$(./FHEv1 -d $cipher_sum $keyfile)
if [ $plain_sum -eq 35 ]; then
   echo The homomorphic addition works correctly!!!
   echo
fi

echo Testing homomorphic multiplication
cipher_product=$(./FHEv1 -m -e 5 -e 7 $keyfile)
plain_product=$(./FHEv1 -d $cipher_product $keyfile)
if [ $plain_product -eq 35 ]; then
   echo The homomorphic multiplication works correctly!!!
   echo
fi

echo Testing the equality test
./FHEv1 -t $cipher_sum $cipher_product $keyfile
./FHEv1 -t -e 34 $cipher_sum $keyfile


echo ---------------------------------------------------------------

keyfile='key_v2.txt';
keysize=96;
w=8;
z=8;

echo Generating the Key File $keyfile for FHEv2
./FHEv2 -k $keysize $w $z $keyfile
echo Key File $keyfile generated!!!
echo

echo Testing the padding
padded=$(./FHEv2 -p 17 $keyfile)
remainder=$(($padded%256))
if [ $remainder -eq 17 ]; then
    echo The padding works correctly!!!
    echo
fi

echo Testing the correctness of encryption and decryption
cipher17=$(./FHEv2 -e 17 $keyfile)
plain17=$(./FHEv2 -d $cipher17 $keyfile)
if [ $plain17 -eq 17 ]; then
   echo The encryption and decryption work correctly!!!
   echo
fi

echo Testing homomorphic addition
cipher_sum=$(./FHEv2 -a $cipher17 -e 18 $keyfile)
plain_sum=$(./FHEv2 -d $cipher_sum $keyfile)
if [ $plain_sum -eq 35 ]; then
   echo The homomorphic addition works correctly!!!
   echo
fi

echo Testing homomorphic multiplication
cipher_product=$(./FHEv2 -m -e 5 -e 7 $keyfile)
plain_product=$(./FHEv2 -d $cipher_product $keyfile)
if [ $plain_product -eq 35 ]; then
   echo The homomorphic multiplication works correctly!!!
   echo
fi