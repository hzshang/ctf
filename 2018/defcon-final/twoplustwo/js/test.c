/*
 * test.c
 * Copyright (C) 2018 hzshang <hzshang15@gmail.com>
 *
 * Distributed under terms of the MIT license.
 */


#include <stdio.h>
#include "duktape.h"

int main(int argc, char *argv[]) {
    duk_context *ctx = duk_create_heap_default();
        

    duk_destroy_heap(ctx);
    return 0;
}
