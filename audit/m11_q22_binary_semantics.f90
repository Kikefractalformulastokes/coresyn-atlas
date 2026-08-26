program m11_q22_binary_semantics
  use iso_fortran_env, only : real32, int32
  implicit none
  real(real32), dimension(8) :: x
  integer :: i

  x = [ 1.0_real32, 0.5_real32, -1.0_real32, 3.1415927_real32, &
        1.0e-20_real32, -1.0e-20_real32, 12345.678_real32, tiny(1.0_real32) ]

  print '(a)', 'label,x,q22,raw_hex,q22_hex,xor_hex,abs_err,rel_err'
  do i=1,size(x)
    call emit(i,x(i))
  end do

contains

  pure elemental function q22(v) result(y)
    real(real32), intent(in) :: v
    real(real32) :: y
    integer(int32) :: raw
    raw = transfer(v,raw)
    raw = ibclr(raw,0)
    y = transfer(raw,y)
  end function q22

  subroutine emit(k,v)
    integer,intent(in) :: k
    real(real32),intent(in) :: v
    real(real32) :: y,ae,re
    integer(int32) :: a,b,d
    y=q22(v); a=transfer(v,a); b=transfer(y,b); d=ieor(a,b)
    ae=abs(y-v)
    if (v /= 0.0_real32) then
       re=ae/abs(v)
    else
       re=ae
    end if
    write(*,'(i0,a,es16.8,a,es16.8,a,z8.8,a,z8.8,a,z8.8,a,es16.8,a,es16.8)') &
      k,',',v,',',y,',',a,',',b,',',d,',',ae,',',re
    if (iand(d,not(1_int32)) /= 0_int32) error stop 'q22 changed a bit other than bit 0'
    if (btest(b,0)) error stop 'q22 failed to clear bit 0'
    if (re > 2.0_real32*epsilon(1.0_real32)) error stop 'relative perturbation unexpectedly large'
  end subroutine emit
end program m11_q22_binary_semantics
